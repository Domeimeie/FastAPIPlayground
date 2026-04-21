from pytest import fixture
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.database import get_session

sqlite_file_name = "database_test.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

SQLModel.metadata.create_all(engine)

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


client = TestClient(app)

@fixture(scope="function", autouse=True)
def clear_database():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def test_read_rot():
    response = client.get("/")
    assert response.status_code == 200

    assert response.json() == {"message": "Welcome to the coolest blog"}

def test_create_user():
    response = client.post("/users", json={"email": "dodododododod@dododod.local", "password":"gagagagaga"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "password" not in data

    user_id = data["id"]
    response = client.get("/users")
    users = response.json()
    assert len(users) == 1
    assert users[0]["id"] == user_id

def test_duplicate_user():
    response = client.post("/users", json={"email": "dodododododod@dododod.local", "password":"gagagagaga"})
    responseDuplicate = client.post("/users", json={"email": "dodododododod@dododod.local", "password":"gagagagaga"})
    assert response.status_code == 200
    assert responseDuplicate.status_code == 409

def test_create_user_no_password():
    response = client.post("/users", json={"email": "dodododododod@dododod.local"})
    assert response.status_code == 422

def test_find_user_by_id():
    client.post("/users", json={"email": "dodododododod@dododod.local", "password":"gagagagaga"})
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "dodododododod@dododod.local"


def test_find_user_by_id_fail():
    response = client.get("/users/1")
    assert response.status_code == 404