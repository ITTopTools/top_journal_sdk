import re
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from top_journal_sdk.exceptions import RequestTimeoutError, translate_http_error


class ApplicationKey:
    """
    Класс для получения и хранения ключа приложения из JavaScript-файлов сайта.

    This class is designed to retrieve and store an application key from the website's JavaScript files.
    It automatically fetches the main page, locates the application JavaScript file,
    and extracts the authentication key using regex patterns.
    """

    def __init__(
        self,
        journal_base_url: str,
        timeout: float = 30.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        """
        Инициализирует экземпляр класса с базовым URL и пустым значением ключа приложения.

        Args:
            journal_base_url: Базовый URL журнала для поиска JavaScript-файлов.
            timeout: Таймаут HTTP-запросов в секундах (для внутреннего клиента).
            client: Внешний HTTP-клиент. Если передан, используется он
                (создание/закрытие не управляется классом); иначе создаётся
                внутренний клиент с указанным таймаутом.

        Initializes the class instance with the base URL and an empty application key value.

        Args:
            journal_base_url: The base URL of the journal for searching JavaScript files.
            timeout: HTTP request timeout in seconds (for the internal client).
            client: External HTTP client. When provided, it is used as-is
                (its lifecycle is not managed by this class); otherwise an
                internal client with the given timeout is created.
        """
        self.journal_base_url: str = journal_base_url
        self.timeout: float = timeout
        self._client: httpx.AsyncClient | None = client
        self._app_key: str = ""

    def _get_js_url(self, root_html: str) -> str:
        """
        Парсит HTML-страницу и находит ссылку на JavaScript-файл приложения.

        Args:
            root_html: HTML-содержимое страницы.

        Returns:
            Полный URL JavaScript-файла приложения или пустую строку, если не найден.

        Parses the HTML page and finds the link to the application JavaScript file.

        Args:
            root_html: HTML content of the page.

        Returns:
            The full URL of the application JavaScript file or an empty string if not found.
        """
        soup = BeautifulSoup(root_html, "html.parser")
        scripts = soup.find_all("script")
        target_script: str = ""
        for script in scripts:
            src = script.get("src")
            if not isinstance(src, str):
                continue
            if src and "app." in src and src.endswith(".js"):
                target_script = src
                break
        if not target_script:
            return ""
        return urljoin(self.journal_base_url, target_script)

    def _get_app_key(self, js_text: str) -> str:
        """
        Извлекает ключ приложения из JavaScript-кода с помощью регулярного выражения.

        Args:
            js_text: Текст JavaScript-файла.

        Returns:
            Извлеченный ключ приложения или пустую строку, если ключ не найден.

        Extracts the application key from JavaScript code using a regular expression.

        Args:
            js_text: The text of the JavaScript file.

        Returns:
            The extracted application key or an empty string if the key is not found.
        """
        pattern = r'o\.authModel\s*=\s*new\s*r\.AuthModel\("([^"]+)"\)'
        match = re.search(pattern, js_text)
        if match:
            token_value = match.group(1)
            return token_value
        else:
            return ""

    async def _retrieve(self, client: httpx.AsyncClient) -> str:
        """
        Выполняет HTTP-запросы для извлечения ключа приложения.

        Performs the HTTP requests to extract the application key.
        """
        root_html_resp = await client.get(self.journal_base_url)
        root_html_resp.raise_for_status()
        js_url = self._get_js_url(root_html_resp.text)
        if not js_url:
            return ""
        js_resp = await client.get(js_url)
        js_resp.raise_for_status()
        return self._get_app_key(js_resp.text)

    async def get_key(self, refresh: bool = False) -> str:
        """
        Получает ключ приложения, при необходимости обновляя его.

        Args:
            refresh: Флаг, указывающий на необходимость принудительного обновления ключа.

        Returns:
            Ключ приложения или пустую строку, если ключ не найден.

        Retrieves the application key, optionally refreshing it if necessary.

        Args:
            refresh: A flag indicating whether to force refresh the key.

        Returns:
            The application key or an empty string if the key is not found.
        """
        if self._app_key == "" or refresh is True:
            try:
                if self._client is not None:
                    app_key = await self._retrieve(self._client)
                else:
                    async with httpx.AsyncClient(timeout=self.timeout) as client:
                        app_key = await self._retrieve(client)
                self._app_key = app_key
                return app_key
            except httpx.TimeoutException as exc:
                raise RequestTimeoutError() from exc
            except httpx.HTTPStatusError as exc:
                mapped = translate_http_error(exc)
                if mapped is None:
                    raise
                raise mapped from exc
        else:
            return self._app_key
