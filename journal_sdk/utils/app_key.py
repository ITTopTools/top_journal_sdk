import re

import httpx
from bs4 import BeautifulSoup


class ApplicationKey:
    def __init__(self):
        self.__base_url: str = "https://journal.top-academy.ru"
        self.__app_js_url: str = ""
        self.__app_token: str | None = ""

    def __parse_index_html(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")
        target_script: str = ""
        for script in scripts:
            src = str(script.get("src"))
            if src and "app." in src and src.endswith(".js"):
                target_script = src
                break
        return target_script

    async def __get_app_js_url(self, refresh: bool = False) -> str:
        if self.__app_js_url == "" or refresh:
            async with httpx.AsyncClient() as client:
                resp = await client.get(self.__base_url)
                script_url = self.__parse_index_html(html=resp.text)
                app_js_url = self.__base_url + script_url
                self.__app_js_url = app_js_url
                return app_js_url
        else:
            return self.__app_js_url

    async def __parse_app_js(self, js_text: str) -> str | None:
        pattern = r'o\.authModel\s*=\s*new\s*r\.AuthModel\("([^"]+)"\)'
        match = re.search(pattern, js_text)
        if match:
            token_value = match.group(1)
            return token_value

    async def get_key(self, refresh: bool = False) -> str | None:
        if self.__app_token == "" or refresh is True:
            async with httpx.AsyncClient() as client:
                resp = await client.get(await self.__get_app_js_url(refresh=True))
                app_token = await self.__parse_app_js(resp.text)
                self.__app_token = app_token
                return app_token
        else:
            return self.__app_token
