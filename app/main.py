import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routes import approvals, auth, balances, hr, leave, reports

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Acme HR Leave Service", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(leave.router)
app.include_router(approvals.router)
app.include_router(balances.router)
app.include_router(hr.router)
app.include_router(reports.router)


@app.get("/health")
def health():
    return {"status": "ok"}
