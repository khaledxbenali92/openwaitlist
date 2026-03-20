"""
Tests for OpenWaitlist
"""

import pytest
from app import create_app, db
from src.models.subscriber import Subscriber


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret",
        "MAIL_SUPPRESS_SEND": True,
        "APP_NAME": "TestApp",
        "ADMIN_PASSWORD": "testpass",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TestApp" in response.data


def test_join_waitlist(client):
    response = client.post("/join", data={
        "email": "test@example.com",
        "name": "Test User"
    }, follow_redirects=True)
    assert response.status_code == 200


def test_duplicate_email(client, app):
    with app.app_context():
        sub = Subscriber(email="existing@example.com")
        db.session.add(sub)
        db.session.commit()

    response = client.post("/join", data={
        "email": "existing@example.com"
    }, follow_redirects=True)
    assert response.status_code == 200


def test_api_stats(client):
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.get_json()
    assert "total_subscribers" in data


def test_api_join(client):
    response = client.post("/api/join",
        json={"email": "api@example.com", "name": "API User"},
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True


def test_referral_code_generated(app):
    with app.app_context():
        sub = Subscriber(email="referral@example.com")
        db.session.add(sub)
        db.session.commit()
        assert sub.referral_code is not None
        assert sub.referral_code.startswith("REF")


def test_position_assigned(app):
    with app.app_context():
        sub1 = Subscriber(email="first@example.com")
        db.session.add(sub1)
        db.session.commit()

        sub2 = Subscriber(email="second@example.com")
        db.session.add(sub2)
        db.session.commit()

        assert sub1.position >= 1
        assert sub2.position >= 1
        assert sub1.id != sub2.id

def test_admin_login(client):
    response = client.post("/admin/login",
        data={"password": "testpass"},
        follow_redirects=True
    )
    assert response.status_code == 200


def test_admin_wrong_password(client):
    response = client.post("/admin/login",
        data={"password": "wrongpass"},
        follow_redirects=False
    )
    assert response.status_code == 200
