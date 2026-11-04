from fastapi import APIRouter, HTTPException

from app import auth
from app.models import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    row = auth.authenticate(body.email, body.password)
    if row is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=auth.create_token(row["id"], row["role"]))
