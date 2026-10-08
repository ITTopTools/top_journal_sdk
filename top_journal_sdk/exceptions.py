import httpx


class JournalException(Exception):
    """Base class for all Journaltop errors."""

    pass


# --- SERVER SIDE ERRORS (5xx) ---
class InternalServerError(JournalException):
    """Raised when the remote server returns 5xx."""

    def __init__(self, status_code: int, message: str = "Server error"):
        self.status_code: int = status_code
        super().__init__(f"{message} (status {status_code})")


# --- INVALIDE AUTH DATA (HTTP 422) ---
class InvalidAuthDataError(JournalException):
    """Raised when the server rejects request data (HTTP 422).

    Most commonly invalid username/password at login, but any endpoint
    may answer 422 on validation failures.
    """

    def __init__(self, status_code: int = 422, message: str = "Invalid request data!"):
        self.status_code: int = status_code
        super().__init__(f"{message} (status {status_code})")


# --- CLIENT SIDE ERRORS (HTTP 404) ---
class DataNotFoundError(JournalException):
    """Raised when requested data/resource was not found."""

    def __init__(
        self,
        url: str | None = None,
        message: str = "Data not found",
        status_code: int = 404,
    ):
        self.url: str | None = url
        self.status_code: int = status_code
        if url is not None:
            message = f"{message}: {url}"
        super().__init__(message)


# --- AUTHORIZATION ERRORS (HTTP 401) ---
class OutdatedJWTError(JournalException):
    """Raised when JWT is outdated."""

    def __init__(self, status_code: int = 401, message: str = "JWT Token outdated! Update JWT!"):
        self.status_code: int = status_code
        super().__init__(f"{message} (status {status_code})")


# --- INVALIDE JWT TOKEN (HTTP 403) ---
class InvalidJWTError(JournalException):
    """Raised when the JWT token is invalid or expired (HTTP 403)."""

    def __init__(
        self,
        status_code: int = 403,
        message: str = "Invalid or expired JWT Token, pls update JWT!",
    ):
        self.status_code: int = status_code
        super().__init__(f"{message} (status {status_code})")


# --- INVALIDE APPLICATION KEY (HTTP 410) ---
class InvalidAppKeyError(JournalException):
    """Raised when the provided app_key is invalid or expired (HTTP 410)."""

    def __init__(self, status_code: int = 410, message: str = "Invalid or expired app_key"):
        self.status_code: int = status_code
        super().__init__(f"{message} (status {status_code})")


# --- TIMEOUT REQUEST ERROR (HTTP 408) ---
class RequestTimeoutError(JournalException):
    """Raised when retry timeout for a request is exceeded."""

    def __init__(self, status_code: int = 408, message: str = "Retry timeout exceeded"):
        self.status_code: int = status_code
        super().__init__(f"{message} (status {status_code})")


# --- LESSON IS MISSING (NoneType) ---
class LessonNotFoundError(JournalException):
    """Raised when the requested lesson is not found in the schedule."""

    def __init__(self, lesson_number: int, message: str | None = None):
        self.lesson_number: int = lesson_number
        if message is None:
            message = f"Lesson number {lesson_number} not found in schedule."
        super().__init__(message)


def translate_http_error(error: httpx.HTTPStatusError) -> JournalException | None:
    """
    Переводит транспортную httpx-ошибку в доменное исключение SDK.

    Translates a transport-level httpx error into an SDK domain exception.

    Args:
        error: Исходная ошибка статуса HTTP / Original HTTP status error.

    Returns:
        Доменное исключение или None, если маппинга для статуса нет
        (вызывающий код должен перевыбросить оригинал).
        Domain exception, or None when there is no mapping for the status
        (the caller should re-raise the original).
    """
    status = error.response.status_code
    if status == 401:
        return OutdatedJWTError()
    if status == 403:
        return InvalidJWTError()
    if status == 404:
        return DataNotFoundError(url=str(error.request.url))
    if status == 408:
        return RequestTimeoutError()
    if status == 410:
        return InvalidAppKeyError()
    if status == 422:
        return InvalidAuthDataError()
    if 500 <= status <= 599:
        return InternalServerError(status)
    return None
