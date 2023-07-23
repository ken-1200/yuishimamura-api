import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_index(ac: AsyncClient):
    response = await ac.get(
        "/",
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_check(ac: AsyncClient):
    response = await ac.get(
        "/health",
    )
    assert response.status_code == 200
