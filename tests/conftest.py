# tests/conftest.py
import os
import pytest
import psycopg2
import alembic.config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db
from app.core.config import settings
from app import schemas, crud

# Ensure test environment variables are loaded before anything else
# (Assumes you have a mechanism in place to load .env.test)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_role():
    conn = psycopg2.connect(settings.PG_ADMIN_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'''
    DO $$
    BEGIN
       IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{settings.ROLE_NAME}') THEN
           CREATE ROLE "{settings.ROLE_NAME}" WITH LOGIN PASSWORD 'password';
       END IF;
    END
    $$;
    ''')
    cursor.close()
    conn.close()

def create_test_database():
    conn = psycopg2.connect(settings.PG_ADMIN_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {settings.DB_NAME}")
    cursor.execute(
        f'CREATE DATABASE {settings.DB_NAME} OWNER "{settings.ROLE_NAME}"')
    cursor.close()
    conn.close()

def drop_test_database():
    conn = psycopg2.connect(settings.PG_ADMIN_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = '{settings.DB_NAME}'
      AND pid <> pg_backend_pid();
    """)
    cursor.execute(f"DROP DATABASE IF EXISTS {settings.DB_NAME}")
    cursor.close()
    conn.close()

def run_migrations():
    alembic.config.main(argv=["upgrade", "head"])

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    create_test_role()
    create_test_database()
    run_migrations()
    yield
    drop_test_database()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def client():
    """Provides a TestClient instance for the test suite."""
    return TestClient(app)

@pytest.fixture(scope="session")
def create_test_user():
    db = TestingSessionLocal()
    user_data = schemas.UserCreate(username="testuser", password="testpassword")
    crud.create_user(db, user_data)
    db.close()

# Centralized fixture to create a test user and get an access token
@pytest.fixture(scope="session")
def access_token(create_test_user, client):
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]
