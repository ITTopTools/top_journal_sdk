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

        jwt: str = await app.login(username="", password="")
        print(f"JWT Token: {jwt}")

        # response = await transport.request( # Manual data fetching wo parsing
        #     method="get",
        #     url=config.JournalEndpoint.USER_INFO.value, 
        #     token=jwt, 
        #     params={"date": "2025-11-01"}
        # )
        sch = await app.get_schedule(token=jwt)
        hw = await app.get_homework(token=jwt)
        prof = await app.get_user_info(token=jwt)
        
        print(hw.total)
        print(sch.lesson(1).teacher_name)
        print(prof.group_name_prop)
        
        # print(f"Server response: {response.json()}")

if __name__ == "__main__":
    asyncio.run(main())
