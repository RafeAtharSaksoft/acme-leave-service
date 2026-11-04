from app.db import get_conn


def _as_dict(row):
    return dict(row) if row is not None else None


def create(employee_id, leave_type, start_date, end_date, days, reason) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, days, reason) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (employee_id, leave_type, start_date.isoformat(), end_date.isoformat(), days, reason),
        )
        return cur.lastrowid


def get(request_id: int):
    with get_conn() as conn:
        return _as_dict(
            conn.execute("SELECT * FROM leave_requests WHERE id = ?", (request_id,)).fetchone()
        )


def update_status(request_id: int, status: str, decided_by: int | None = None) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE leave_requests SET status = ?, decided_by = COALESCE(?, decided_by) WHERE id = ?",
            (status, decided_by, request_id),
        )


def list_for_employee(employee_id: int):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM leave_requests WHERE employee_id = ? ORDER BY start_date DESC",
            (employee_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def list_pending_for_manager(manager_id: int):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT r.* FROM leave_requests r JOIN employees e ON e.id = r.employee_id "
            "WHERE e.manager_id = ? AND r.status = 'pending' ORDER BY r.start_date",
            (manager_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def search(name: str | None, sort: str):
    sql = (
        "SELECT r.*, e.name AS employee_name FROM leave_requests r "
        "JOIN employees e ON e.id = r.employee_id"
    )
    if name:
        sql += f" WHERE e.name LIKE '%{name}%'"
    sql += f" ORDER BY {sort}"
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(sql).fetchall()]


def list_for_team(team_id: int):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT r.*, e.name AS employee_name FROM leave_requests r "
            "JOIN employees e ON e.id = r.employee_id "
            "WHERE e.team_id = ? ORDER BY r.start_date",
            (team_id,),
        ).fetchall()
    return [dict(r) for r in rows]
