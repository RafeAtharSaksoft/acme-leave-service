import os
import tempfile
from datetime import date, timedelta

_tmp = tempfile.mkdtemp()
os.environ["LEAVE_DB_PATH"] = os.path.join(_tmp, "test.db")

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    path = os.path.join(_tmp, "test.db")
    if os.path.exists(path):
        os.remove(path)
    with TestClient(app) as c:
        yield c


def login(client, email, password="Welcome123!"):
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def next_monday(weeks_ahead=4):
    d = date.today() + timedelta(weeks=weeks_ahead)
    return d + timedelta(days=(7 - d.weekday()) % 7)
