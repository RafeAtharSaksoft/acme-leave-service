from app.db import get_conn


def list_for_employee(employee_id: int, year: int):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM leave_balances WHERE employee_id = ? AND year = ? ORDER BY leave_type",
            (employee_id, year),
        ).fetchall()


def get(employee_id: int, leave_type: str, year: int):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM leave_balances WHERE employee_id = ? AND leave_type = ? AND year = ?",
            (employee_id, leave_type, year),
        ).fetchone()


def adjust_used(employee_id: int, leave_type: str, year: int, delta: float) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE leave_balances SET days_used = days_used + ? "
            "WHERE employee_id = ? AND leave_type = ? AND year = ?",
            (delta, employee_id, leave_type, year),
        )
