from typing import List

from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models import CurrentUser, LeaveRequestCreate, LeaveRequestOut
from app.services import leave_service

router = APIRouter(prefix="/leave-requests", tags=["leave"])


@router.post("", response_model=LeaveRequestOut, status_code=201)
def create(body: LeaveRequestCreate, user: CurrentUser = Depends(get_current_user)):
    return leave_service.create_request(user, body)


@router.get("/mine", response_model=List[LeaveRequestOut])
def mine(user: CurrentUser = Depends(get_current_user)):
    return leave_service.list_mine(user)


@router.get("/{request_id}", response_model=LeaveRequestOut)
def get_one(request_id: int, user: CurrentUser = Depends(get_current_user)):
    return leave_service.get_request(user, request_id)


@router.post("/{request_id}/cancel", response_model=LeaveRequestOut)
def cancel(request_id: int, user: CurrentUser = Depends(get_current_user)):
    return leave_service.cancel(user, request_id)
