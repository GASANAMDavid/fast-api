from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import uuid

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    unique_username = f"testuser_{uuid.uuid4()}"
    response = client.post(
        "/users/",
        json={"username": unique_username, "password": "testpassword"}
    )
    print(response.json())  # Add this line to print the response content
    assert response.status_code == 200
    assert response.json()["username"] == unique_username


def test_login():
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_create_item():
    token_response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = token_response.json()["access_token"]
    response = client.post(
        "/items/",
        json={"title": "Test Item", "description": "This is a test item"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Item"


def test_read_items():
    token_response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = token_response.json()["access_token"]
    response = client.get(
        "/items/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_update_item():
    token_response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = token_response.json()["access_token"]
    response = client.put(
        "/items/1",
        json={"title": "Updated Test Item",
              "description": "This is an updated test item"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Item"


def test_delete_item():
    token_response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = token_response.json()["access_token"]
    response = client.delete(
        "/items/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Item"
