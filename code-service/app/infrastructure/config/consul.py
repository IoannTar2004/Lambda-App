import httpx
from fastapi import HTTPException

from settings import settings


consul_url = f"http://{settings.CONSUL_HOST}:{settings.CONSUL_PORT}"

async def service_register() -> None:
    async with httpx.AsyncClient() as client:
        res = await client.put(
            f"{consul_url}/v1/agent/service/register",
            json={
                "ID": settings.SERVICE_NAME,
                "Name": settings.SERVICE_NAME,
                "Address": settings.ACCESS_HOST,
                "Port": int(settings.ACCESS_PORT),
                "Check": {
                    "HTTP": f"http://{settings.ACCESS_HOST}:{int(settings.ACCESS_PORT)}/health",
                    "Interval": "10s"
                }
            }
        )
        res.raise_for_status()

async def get_service_url(service_name: str) -> str:
    if not service_name:
        return ""

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{consul_url}/v1/health/service/{service_name}")
        if not res.json():
            raise HTTPException(status_code=404, detail="Service not found")

        service = res.json()[0]["Service"]
        return f"http://{service['Address']}:{service['Port']}"

async def service_unregister() -> None:
    async with httpx.AsyncClient() as client:
        await client.put(f"{consul_url}/v1/agent/service/deregister/{settings.SERVICE_NAME}", json={})