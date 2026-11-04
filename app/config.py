import os

DB_PATH = os.getenv("LEAVE_DB_PATH", "leave.db")

JWT_SECRET = os.getenv("LEAVE_JWT_SECRET", "acme-hr-leave-secret-2023")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_DAYS = 30

DEFAULT_ANNUAL_DAYS = 25
DEFAULT_SICK_DAYS = 10
