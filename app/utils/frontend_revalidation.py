from typing import List
import httpx

from app.core import settings


async def revalidate_frontend(tags: List[str]):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.front_end_url}/api/revalidate", json={"tags": tags})
    if response.status_code != 200:
        print("error revalidation")
