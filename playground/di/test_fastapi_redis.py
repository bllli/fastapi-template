import asyncio
from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio

from di.fastapi_redis import create_app


@pytest_asyncio.fixture(scope="session")
async def client():
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.asyncio(loop_scope="session")
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"result": "locked"}


@pytest.mark.asyncio(loop_scope="session")
async def test_root_2(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"result": "locked"}


@pytest.mark.asyncio(loop_scope="session")
async def test_root_3(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"result": "locked"}
