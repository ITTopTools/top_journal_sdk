# THIS IS TEST FILE
# TO RUN - Go to root project and uv sync&&uv run python -m src

import asyncio

import httpx

from journaltop.client import Client
from journaltop.data import config
from journaltop.transport import Transport


async def main():
    async with httpx.AsyncClient() as client:
        app = Client(client)
        transport = Transport(client)

        jwt: str = await app.login(username="username", password="password")
        print(f"JWT Token: {jwt}")

        response = await transport.request( # Manual data fetching wo parsing
            method="get",
            url=config.JournalEndpoint.STUDENT_HOMEWORK.value, 
            token=jwt, 
            params={"date": "2025-11-01"}
        )

        print(f"Server response: {response.json()}")

        result1 = await app.get_schedule(token=jwt, date=None)
        result2 = await app.get_schedule(token=jwt, date="2025-10-30")
        
        print(result1.lesson(1).started_at)

        await app.close_connection()

        print(f"{result1}\n")
        print(f"{result2}\n")

if __name__ == "__main__":
    asyncio.run(main())
