from .base import JournalError


# --- SERVER SIDE ERRORS (5xx) ---
class JournalInternalServerError(JournalError):
    """Raised when the remote server returns 5xx."""
    def __init__(self, status_code: int, message: str = "Server error"):
        self.status_code = status_code
        super().__init__(f"{message} (status {status_code})")


# --- AUTHENTICATION / AUTHORIZATION ERRORS (401/403) ---
class JournalAuthError(JournalError):
    """Raised when authentication or authorization fails."""
    def __init__(self, message: str = "Authorization failed"):
        super().__init__(message)


# --- CLIENT SIDE ERRORS (4xx) ---
class JournalNotFoundError(JournalError):
    """Raised when requested data/resource was not found."""
    def __init__(self, url: str | None = None, message: str = "Data not found"):
        self.url = url
        if url:
            message = f"{message}: {url}"
        super().__init__(message)


# --- USER MISUSE / SDK MISUSE ---
class JournalInvalidUsageError(JournalError):
    """Raised when the SDK is used incorrectly by the client."""
    def __init__(self, message: str = "Invalid SDK usage"):
        super().__init__(message)


# --- INVALIDE APPLICATION KEY
class InvalidAppKeyError(JournalError):
    """Raised when the provided app_key is invalid or expired (HTTP 410)."""
    def __init__(self, status_code: int = 410, message: str = "Invalid or expired app_key"):
        self.status_code = status_code
        super().__init__(f"{message} (status {status_code})")

# --- INVALIDE APPLICATION KEY
class RequestTimeoutError(JournalError):
    """Raised when the provided app_key is invalid or expired (HTTP 410)."""
    def __init__(self, status_code: int = 410, message: str = "Invalid or expired app_key"):
        self.status_code = status_code
        super().__init__(f"{message} (status {status_code})")


# --- TIMEOUT REQUEST ERROR 
class RequestTimeoutError(JournalError):
    """Raised when retry timeout for a request is exceeded."""
    def __init__(self, message: str = "Retry timeout exceeded"):
        super().__init__(message)
