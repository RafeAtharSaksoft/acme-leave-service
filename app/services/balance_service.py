from datetime import date, timedelta

from app.repositories import balances


def working_days(start: date, end: date) -> int:
    """Number of Monday-Friday days between start and end, inclusive."""
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            count += 1
        current += timedelta(days=1)
    return count


def list_balances(employee_id: int, year: int):
    return [
        {
            "leave_type": b["leave_type"],
            "year": b["year"],
            "days_total": b["days_total"],
            "days_used": b["days_used"],
            "days_remaining": b["days_total"] - b["days_used"],
        }
        for b in balances.list_for_employee(employee_id, year)
    ]


def has_enough(employee_id: int, leave_type: str, year: int, days: float) -> bool:
    if leave_type == "unpaid":
        return True
    row = balances.get(employee_id, leave_type, year)
    return row is not None and row["days_total"] - row["days_used"] >= days


def deduct(employee_id: int, leave_type: str, year: int, days: float) -> None:
    if leave_type != "unpaid":
        balances.adjust_used(employee_id, leave_type, year, days)


def restore(employee_id: int, leave_type: str, year: int, days: float) -> None:
    if leave_type != "unpaid":
        balances.adjust_used(employee_id, leave_type, year, -days)
