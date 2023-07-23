import os
from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.settings import Settings

settings = Settings()


@pytest.fixture
async def ac() -> AsyncGenerator:
    headers = {"X-YUISHIMAMURA-API-KEY": settings.API_KEY}
    async with AsyncClient(app=app, base_url="https://test", headers=headers) as c:
        yield c


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        c.headers.update({"X-YUISHIMAMURA-API-KEY": settings.API_KEY})
        yield c


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "ap-northeast-1"
