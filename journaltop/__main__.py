# THIS IS TEST FILE
# TO RUN - Go to root project and uv sync&&uv run python -m src

import asyncio
import httpx

from journaltop.client import Client
from journaltop.transport import Transport
from journaltop.data import config


async def main():
    async with httpx.AsyncClient() as client:
        app = Client(client)
        transport = Transport(client)

        jwt = await app.login(username="atama_dy40", password="w08n2MP6KBfE")

        response = await transport.request(
            "get", config.JournalEndpoint.METRIC_GRADE.value, token=jwt
            )

        print(f"JWT Token: {jwt}")
        print(f"Server response: {response.json()}")


if __name__ == "__main__":
    asyncio.run(main())
