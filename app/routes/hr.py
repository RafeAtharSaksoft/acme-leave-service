from typing import List, Optional

from fastapi import APIRouter, Depends

from app.auth import require_roles
from app.models import CurrentUser
from app.services import leave_service

router = APIRouter(prefix="/hr", tags=["hr"])


@router.get("/leave-requests")
def search_requests(
    name: Optional[str] = None,
    sort: str = "r.start_date",
    user: CurrentUser = Depends(require_roles("hr_admin")),
) -> List[dict]:
    rows = leave_service.search(name, sort)
    return rows
