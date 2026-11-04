from dataclasses import dataclass
from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field

LeaveType = Literal["annual", "sick", "unpaid"]


@dataclass
class CurrentUser:
    id: int
    name: str
    email: str
    role: str
    manager_id: Optional[int]
    team_id: int


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LeaveRequestCreate(BaseModel):
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: Optional[str] = Field(default=None, max_length=1000)


class LeaveRequestOut(BaseModel):
    id: int
    employee_id: int
    leave_type: LeaveType
    start_date: date
    end_date: date
    days: float
    reason: Optional[str]
    status: str
    decided_by: Optional[int]


class BalanceOut(BaseModel):
    leave_type: str
    year: int
    days_total: float
    days_used: float
    days_remaining: float
