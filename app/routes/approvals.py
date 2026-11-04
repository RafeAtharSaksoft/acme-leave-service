from typing import List

from fastapi import APIRouter, Depends

from app.auth import require_roles
from app.models import CurrentUser, LeaveRequestOut
from app.services import leave_service

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.get("/pending", response_model=List[LeaveRequestOut])
def pending(user: CurrentUser = Depends(require_roles("manager"))):
    return leave_service.pending_for_manager(user)


@router.post("/{request_id}/approve", response_model=LeaveRequestOut)
def approve(request_id: int, user: CurrentUser = Depends(require_roles("manager"))):
    return leave_service.approve(user, request_id)


@router.post("/{request_id}/reject", response_model=LeaveRequestOut)
def reject(request_id: int, user: CurrentUser = Depends(require_roles("manager"))):
    return leave_service.reject(user, request_id)
