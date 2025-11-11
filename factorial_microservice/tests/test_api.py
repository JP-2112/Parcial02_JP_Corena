import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_factorial_ok():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/factorial?n=5")
    assert resp.status_code == 200
    data = resp.json()
    assert data["numero"] == 5
    assert data["factorial"] == "120"
    assert data["paridad"] == "par"

@pytest.mark.asyncio
async def test_factorial_negative():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/factorial?n=-1")
    assert resp.status_code == 400
