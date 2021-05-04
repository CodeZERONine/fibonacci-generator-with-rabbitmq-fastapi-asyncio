import pytest
from httpx import AsyncClient
from fastapi import status
from asyncio import get_event_loop

from main import app

import math

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client

@pytest.fixture(scope="module")
def event_loop():
    loop = get_event_loop()
    yield loop

def is_fibonacci(n):
    phi = 0.5 + 0.5 * math.sqrt(5.0)
    a = phi * n
    return n == 0 or abs(round(a) - a) < 1.0 / n

@pytest.mark.asyncio
async def test_get_fibonacci_number(async_client: AsyncClient) -> None:
    response = await async_client.get("/fibonacci/")
    assert response.status_code == status.HTTP_200_OK
    assert is_fibonacci(response.json())