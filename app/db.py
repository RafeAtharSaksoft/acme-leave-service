import hashlib
import os
import sqlite3
from contextlib import contextmanager
from datetime import date

from app import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('employee', 'manager', 'hr_admin')),
    manager_id INTEGER REFERENCES employees(id),
    team_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS leave_balances (
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    leave_type TEXT NOT NULL,
    year INTEGER NOT NULL,
    days_total REAL NOT NULL,
    days_used REAL NOT NULL DEFAULT 0,
    PRIMARY KEY (employee_id, leave_type, year)
);

CREATE TABLE IF NOT EXISTS leave_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    leave_type TEXT NOT NULL CHECK (leave_type IN ('annual', 'sick', 'unpaid')),
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    days REAL NOT NULL,
    reason TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    decided_by INTEGER REFERENCES employees(id),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

SEED_PASSWORD = "Welcome123!"

# (name, email, role, manager email, team)
SEED_EMPLOYEES = [
    ("Priya Nair", "priya.nair@acme.example", "hr_admin", None, 1),
    ("Dan Owens", "dan.owens@acme.example", "manager", "priya.nair@acme.example", 2),
    ("Maria Silva", "maria.silva@acme.example", "manager", "priya.nair@acme.example", 3),
    ("Alice Chen", "alice.chen@acme.example", "employee", "dan.owens@acme.example", 2),
    ("Bob Okafor", "bob.okafor@acme.example", "employee", "dan.owens@acme.example", 2),
    ("Carol Evans", "carol.evans@acme.example", "employee", "maria.silva@acme.example", 3),
]


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return salt.hex() + "$" + digest.hex()


def verify_password(password: str, stored: str) -> bool:
    salt_hex, _, digest_hex = stored.partition("$")
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 100_000)
    return candidate.hex() == digest_hex


@contextmanager
def get_conn():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        if conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0] == 0:
            _seed(conn)


def _seed(conn: sqlite3.Connection) -> None:
    ids = {}
    for name, email, role, manager_email, team in SEED_EMPLOYEES:
        manager_id = ids.get(manager_email)
        cur = conn.execute(
            "INSERT INTO employees (name, email, password_hash, role, manager_id, team_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (name, email, hash_password(SEED_PASSWORD), role, manager_id, team),
        )
        ids[email] = cur.lastrowid
    year = date.today().year
    for emp_id in ids.values():
        for leave_type, total in (
            ("annual", config.DEFAULT_ANNUAL_DAYS),
            ("sick", config.DEFAULT_SICK_DAYS),
        ):
            for y in (year, year + 1):
                conn.execute(
                    "INSERT INTO leave_balances (employee_id, leave_type, year, days_total, days_used) "
                    "VALUES (?, ?, ?, ?, 0)",
                    (emp_id, leave_type, y, total),
                )
