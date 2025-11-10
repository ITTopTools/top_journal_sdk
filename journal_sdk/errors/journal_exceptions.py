from journal_sdk.errors.base import JournalError


# --- SERVER SIDE ERRORS (5xx) ---
class InternalServerError(JournalError):
    """Raised when the remote server returns 5xx."""

    def __init__(self, status_code: int, message: str = "Server error"):
        self.status_code: int = status_code
        super().__init__(f"{message} (status {status_code})")


# --- INVALIDE AUTH DATA (HTTP 422) ---
class InvalidAuthDataError(JournalError):
    """Raised when the provided username or password is invalid or expired (HTTP 422)."""

    def __init__(self, status_code: int = 422, message: str = "Invalid login data!"):
        self.status_code: int = status_code
        super().__init__(f"{message} (status {status_code})")


# --- CLIENT SIDE ERRORS (HTTP 404) ---
class DataNotFoundError(JournalError):
    """Raised when requested data/resource was not found."""

    def __init__(self, url: str | None = None, message: str = "Data not found"):
        self.url: str | None = url
        if url:
            message = f"{message}: {url}"
        super().__init__(message)


# --- AUTHORIZATION ERRORS (HTTP 401) ---
class OutdatedJWTError(JournalError):
    """Raised when JWT is outdated."""

    def __init__(
        self, status_code: int = 401, message: str = "JWT Token outdated! Update JWT!"
    ):
        super().__init__(f"{message} (status {status_code})")


# --- INVALIDE JWT TOKEN (HTTP 403) ---
class InvalidJWTError(JournalError):
    """Raised when the JWT token is invalid or expired (HTTP 403)."""

    def __init__(
        self,
        status_code: int = 403,
        message: str = "Invalid or expired JWT Token, pls update JWT!",
    ):
        self.status_code: int = status_code
        super().__init__(f"{message} (status {status_code})")


# --- INVALIDE APPLICATION KEY (HTTP 410) ---
class InvalidAppKeyError(JournalError):
    """Raised when the provided app_key is invalid or expired (HTTP 410)."""

    def __init__(
        self, status_code: int = 410, message: str = "Invalid or expired app_key"
    ):
        self.status_code: int = status_code
        super().__init__(f"{message} (status {status_code})")


# --- TIMEOUT REQUEST ERROR (HTTP 408) ---
class RequestTimeoutError(JournalError):
    """Raised when retry timeout for a request is exceeded."""

    def __init__(self, status_code: int = 408, message: str = "Retry timeout exceeded"):
        super().__init__(f"{message} (status {status_code})")


# --- LESSON IS MISSING (NoneType) ---
class LessonNotFoundError(JournalError):
    """Raised when the requested lesson is not found in the schedule."""

    def __init__(self, lesson_number: int, message: str | None = None):
        self.lesson_number = lesson_number
        if message is None:
            message = f"Lesson number {lesson_number} not found in schedule."
        super().__init__(message)
