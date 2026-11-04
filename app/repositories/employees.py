from app.db import get_conn


def get_by_id(employee_id: int):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM employees WHERE id = ?", (employee_id,)).fetchone()


def get_by_email(email: str):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM employees WHERE email = ?", (email,)).fetchone()
