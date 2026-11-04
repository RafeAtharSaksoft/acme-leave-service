from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app import config
from app.db import verify_password
from app.models import CurrentUser
from app.repositories import employees

bearer = HTTPBearer(auto_error=False)


def authenticate(email: str, password: str):
    row = employees.get_by_email(email)
    if row is None or not verify_password(password, row["password_hash"]):
        return None
    return row


def create_token(employee_id: int, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(employee_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(days=config.TOKEN_EXPIRY_DAYS),
    }
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> CurrentUser:
    if creds is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(creds.credentials, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    row = employees.get_by_id(int(payload["sub"]))
    if row is None:
        raise HTTPException(status_code=401, detail="Unknown user")
    return CurrentUser(
        id=row["id"],
        name=row["name"],
        email=row["email"],
        role=row["role"],
        manager_id=row["manager_id"],
        team_id=row["team_id"],
    )


def require_roles(*roles: str):
    def checker(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user

    return checker
