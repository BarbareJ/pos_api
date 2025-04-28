import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.database import Base, engine

@pytest.fixture(scope="session", autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as c:
        yield c


