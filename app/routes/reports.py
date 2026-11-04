import csv
import io

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.auth import require_roles
from app.models import CurrentUser
from app.repositories import leave_requests

router = APIRouter(prefix="/reports", tags=["reports"])

CSV_COLUMNS = ["request_id", "employee", "leave_type", "start_date", "end_date", "days", "status", "reason"]


@router.get("/team/{team_id}/leave.csv")
def team_leave_csv(team_id: int, user: CurrentUser = Depends(require_roles("manager"))):
    rows = leave_requests.list_for_team(team_id)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(CSV_COLUMNS)
    for r in rows:
        writer.writerow(
            [r["id"], r["employee_name"], r["leave_type"], r["start_date"], r["end_date"],
             r["days"], r["status"], r["reason"] or ""]
        )
    return Response(
        content=buf.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="team-{team_id}-leave.csv"'},
    )
