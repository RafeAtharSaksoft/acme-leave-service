import os

DB_PATH = os.getenv("LEAVE_DB_PATH", "leave.db")

JWT_SECRET = os.environ["LEAVE_JWT_SECRET"]  # required; the service refuses to start without it
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_DAYS = 30

DEFAULT_ANNUAL_DAYS = 25
DEFAULT_SICK_DAYS = 10
