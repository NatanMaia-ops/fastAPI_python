from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


# bloco de teste de codigo reutilizavel
@pytest.fixture
def client():
    return TestClient(app)


def test_read_root(client):

    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


def test_create_user(client):
    client = TestClient(app)
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 1,
    }


def read_users(client):

    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "alice",
                "email": "alice@example.com",
                "id": 1,
            },
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_update_user_404(client):
    response = client.put(
        "/users/999",
        json={"username": "err", "email": "err@ex.com", "password": "123"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user_ok(client):
    client.post(
        "/users/",
        json={"username": "zap", "email": "z@z.com", "password": "123"},
    )

    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == "zap"


def test_delete_user_404(client):
    response = client.delete("/users/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
