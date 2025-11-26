import re

import httpx
from bs4 import BeautifulSoup


class ApplicationKey:
    """Класс для получения и хранения ключа приложения из JavaScript-файлов сайта."""

    def __init__(self, journal_base_url: str) -> None:
        """Инициализирует экземпляр класса с базовым URL и пустым значением ключа приложения.

        Args:
            journal_base_url: Базовый URL журнала для поиска JavaScript-файлов.
        """
        self.journal_base_url: str = journal_base_url
        self.__app_key: str = ""

    def __get_js_url(self, root_html: str) -> str:
        """
        Парсит HTML-страницу и находит ссылку на JavaScript-файл приложения.

        Args:
            root_html: HTML-содержимое страницы.

        Returns:
            Полный URL JavaScript-файла приложения или пустую строку, если не найден.
        """
        soup = BeautifulSoup(root_html, "html.parser")
        scripts = soup.find_all("script")
        target_script: str = ""
        for script in scripts:
            src = str(script.get("src"))
            if src and "app." in src and src.endswith(".js"):
                target_script = src
                break
        return self.journal_base_url + target_script

    async def __get_app_key(self, js_text: str) -> str:
        """
        Извлекает ключ приложения из JavaScript-кода с помощью регулярного выражения.

        Args:
            js_text: Текст JavaScript-файла.

        Returns:
            Извлеченный ключ приложения или пустую строку, если ключ не найден.
        """
        pattern = r'o\.authModel\s*=\s*new\s*r\.AuthModel\("([^"]+)"\)'
        match = re.search(pattern, js_text)
        if match:
            token_value = match.group(1)
            return token_value
        else:
            return ""

    async def get_key(self, refresh: bool = False) -> str:
        """
        Получает ключ приложения, при необходимости обновляя его.

        Args:
            refresh: Флаг, указывающий на необходимость принудительного обновления ключа.

        Returns:
            Ключ приложения или пустую строку, если ключ не найден.
        """
        if self.__app_key == "" or refresh is True:
            async with httpx.AsyncClient() as client:
                root_html_resp = await client.get(self.journal_base_url)
                js_url = self.__get_js_url(root_html_resp.text)
                js_resp = await client.get(js_url)
                app_key = await self.__get_app_key(js_resp.text)
                self.__app_key = app_key
                return app_key
        else:
            return self.__app_key
