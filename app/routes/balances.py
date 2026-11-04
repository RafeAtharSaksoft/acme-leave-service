from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models import BalanceOut, CurrentUser
from app.services import balance_service

router = APIRouter(prefix="/balances", tags=["balances"])


@router.get("/me", response_model=List[BalanceOut])
def my_balances(year: Optional[int] = None, user: CurrentUser = Depends(get_current_user)):
    return balance_service.list_balances(user.id, year or date.today().year)
