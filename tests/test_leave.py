from datetime import timedelta

from tests.conftest import login, next_monday


def test_login_and_balances(client):
    h = login(client, "alice.chen@acme.example")
    r = client.get("/balances/me", headers=h)
    assert r.status_code == 200
    annual = next(b for b in r.json() if b["leave_type"] == "annual")
    assert annual["days_remaining"] == 25


def test_create_leave_request(client):
    h = login(client, "alice.chen@acme.example")
    start = next_monday()
    r = client.post(
        "/leave-requests",
        json={"leave_type": "annual", "start_date": str(start),
              "end_date": str(start + timedelta(days=4)), "reason": "Family trip"},
        headers=h,
    )
    assert r.status_code == 201
    assert r.json()["status"] == "pending"
    assert r.json()["days"] == 5


def test_manager_approves_report_request(client):
    alice = login(client, "alice.chen@acme.example")
    dan = login(client, "dan.owens@acme.example")
    start = next_monday()
    req = client.post(
        "/leave-requests",
        json={"leave_type": "annual", "start_date": str(start),
              "end_date": str(start + timedelta(days=1)), "reason": "Holiday"},
        headers=alice,
    ).json()
    r = client.post(f"/approvals/{req['id']}/approve", headers=dan)
    assert r.status_code == 200
    assert r.json()["status"] == "approved"
    balances = client.get("/balances/me", headers=alice).json()
    annual = next(b for b in balances if b["leave_type"] == "annual")
    assert annual["days_used"] == 2
