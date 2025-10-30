# THIS IS TEST FILE
# TO RUN - Go to root project and uv sync&&uv run python -m src

import asyncio
import httpx

from src.client import Client
from src.transport import Transport
from src.data import config


async def main():
    async with httpx.AsyncClient() as client:
        app = Client(client)
        transport = Transport(client)

        jwt = await app.login(username="username", password="password")

        response = await transport.request("get", config.STUDENT_HOMEWORK, token=jwt)

        print(f"JWT Token: {jwt}")
        print(f"Server response: {response.json()}")


if __name__ == "__main__":
    asyncio.run(main())
