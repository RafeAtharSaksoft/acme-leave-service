import logging
from datetime import date

from fastapi import HTTPException

from app.models import CurrentUser, LeaveRequestCreate
from app.repositories import employees, leave_requests
from app.services import balance_service

logger = logging.getLogger("leave")


def _get_or_404(request_id: int):
    row = leave_requests.get(request_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return row


def create_request(user: CurrentUser, payload: LeaveRequestCreate):
    if payload.end_date < payload.start_date:
        raise HTTPException(status_code=422, detail="end_date must not be before start_date")
    days = balance_service.working_days(payload.start_date, payload.end_date)
    if days == 0:
        raise HTTPException(status_code=422, detail="Request contains no working days")
    if not balance_service.has_enough(user.id, payload.leave_type, payload.start_date.year, days):
        raise HTTPException(status_code=409, detail="Insufficient leave balance")
    request_id = leave_requests.create(
        user.id, payload.leave_type, payload.start_date, payload.end_date, days, payload.reason
    )
    logger.info(
        "Leave request %s created by %s (%s): %s %s to %s, reason=%r",
        request_id, user.email, user.name, payload.leave_type,
        payload.start_date, payload.end_date, payload.reason,
    )
    return leave_requests.get(request_id)


def list_mine(user: CurrentUser):
    return leave_requests.list_for_employee(user.id)


def get_request(user: CurrentUser, request_id: int):
    row = _get_or_404(request_id)
    owner = employees.get_by_id(row["employee_id"])
    allowed = (
        row["employee_id"] == user.id
        or user.role == "hr_admin"
        or (user.role == "manager" and owner["manager_id"] == user.id)
    )
    if not allowed:
        raise HTTPException(status_code=403, detail="Not allowed to view this request")
    return row


def pending_for_manager(user: CurrentUser):
    return leave_requests.list_pending_for_manager(user.id)


def _require_direct_report(manager: CurrentUser, row) -> None:
    owner = employees.get_by_id(row["employee_id"])
    if owner["id"] == manager.id:
        raise HTTPException(status_code=403, detail="You cannot decide your own request")
    if owner["manager_id"] != manager.id:
        raise HTTPException(status_code=403, detail="Not your direct report")


def approve(manager: CurrentUser, request_id: int):
    row = _get_or_404(request_id)
    if row["status"] != "pending":
        raise HTTPException(status_code=409, detail="Only pending requests can be approved")
    year = date.fromisoformat(row["start_date"]).year
    if not balance_service.has_enough(row["employee_id"], row["leave_type"], year, row["days"]):
        raise HTTPException(status_code=409, detail="Insufficient leave balance")
    balance_service.deduct(row["employee_id"], row["leave_type"], year, row["days"])
    leave_requests.update_status(request_id, "approved", manager.id)
    owner = employees.get_by_id(row["employee_id"])
    logger.info(
        "Leave request %s approved by %s for %s (%s), reason=%r",
        request_id, manager.email, owner["email"], owner["name"], row["reason"],
    )
    return leave_requests.get(request_id)


def reject(manager: CurrentUser, request_id: int):
    row = _get_or_404(request_id)
    _require_direct_report(manager, row)
    if row["status"] != "pending":
        raise HTTPException(status_code=409, detail="Only pending requests can be rejected")
    leave_requests.update_status(request_id, "rejected", manager.id)
    logger.info("Leave request %s rejected by %s", request_id, manager.email)
    return leave_requests.get(request_id)


def cancel(user: CurrentUser, request_id: int):
    row = _get_or_404(request_id)
    if row["employee_id"] != user.id:
        raise HTTPException(status_code=403, detail="Only the requester can cancel")
    leave_requests.update_status(request_id, "cancelled")
    logger.info(
        "Leave request %s cancelled by %s, reason=%r", request_id, user.email, row["reason"]
    )
    return leave_requests.get(request_id)


def search(name: str | None, sort: str):
    return leave_requests.search(name, sort)
