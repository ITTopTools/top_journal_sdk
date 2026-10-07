from typing import TypeVar, cast

from httpx import AsyncClient

from top_journal_sdk.controllers import (
    AttendanceController,
    AuthController,
    DashboardController,
    ExamsController,
    FeedbackController,
    GradesController,
    HomeworkController,
    LeaderboardController,
    LessonEvaluationController,
    ScheduleController,
    UserInfoController,
)
from top_journal_sdk.enums.endpoints import JournalEndpoints
from top_journal_sdk.enums.headers import JournalHeaders
from top_journal_sdk.exceptions import OutdatedJWTError
from top_journal_sdk.models.auth import LoginRequest, RefreshTokenRequest
from top_journal_sdk.rapid.client import BaseController
from top_journal_sdk.session import SessionContext
from top_journal_sdk.utils.app_key import ApplicationKey

DEFAULT_TIMEOUT: float = 30.0

T = TypeVar("T", bound=BaseController)


class TopJournalSDK:
    """
    Основной класс SDK для взаимодействия с Top Academy Journal API.

    Main SDK class for interacting with Top Academy Journal API.
    """

    def __init__(
        self,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ):
        """
        Инициализирует SDK с пустыми значениями контроллеров.

        Initialize the SDK with empty controller values.

        Args:
            timeout: Таймаут HTTP-запросов в секундах / HTTP request timeout in seconds.
            user_agent: Переопределение User-Agent / User-Agent override.
            extra_headers: Дополнительные заголовки поверх стандартных /
                Extra headers merged over the defaults.
        """
        self._timeout: float = timeout
        self._user_agent: str | None = user_agent
        self._extra_headers: dict[str, str] = dict(extra_headers) if extra_headers else {}
        self._client: AsyncClient | None = None
        self._auth_controller: AuthController | None = None
        self._attendance_controller: AttendanceController | None = None
        self._lesson_evaluation_controller: LessonEvaluationController | None = None
        self._feedback_controller: FeedbackController | None = None
        self._grades_controller: GradesController | None = None
        self._homework_controller: HomeworkController | None = None
        self._leaderboard_controller: LeaderboardController | None = None
        self._schedule_controller: ScheduleController | None = None
        self._user_info_controller: UserInfoController | None = None
        self._dashboard_controller: DashboardController | None = None
        self._exams_controller: ExamsController | None = None
        self._controller_names: set[str] = set()
        self._session = SessionContext()
        self._refresh_token: str | None = None

    async def __aenter__(self) -> "TopJournalSDK":
        """
        Асинхронный контекстный менеджер: вход.

        Async context manager entry.
        """
        await self.initialize()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """
        Асинхронный контекстный менеджер: выход.

        Async context manager exit.
        """
        await self.close()

    async def initialize(self) -> None:
        """
        Инициализирует SDK: создаёт HTTP-клиент и устанавливает заголовки.

        Initialize the SDK with proper client and headers.

        Повторный вызов без close() — no-op, существующий клиент переиспользуется.
        Calling twice without close() is a no-op, the existing client is reused.
        """
        if self._client is not None:
            return
        client = AsyncClient(
            base_url=JournalEndpoints.API_BASE_URL.value,
            follow_redirects=True,
            timeout=self._timeout,
        )
        headers: dict[str, str] = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": JournalHeaders.ORIGIN.value,
            "Referer": JournalHeaders.REFERER.value,
            "User-Agent": self._user_agent or JournalHeaders.USER_AGENT.value,
        }
        headers.update(self._extra_headers)
        client.headers.update(headers)
        self._client = client

    def set_auth_token(self, token: str) -> None:
        """
        Устанавливает токен авторизации для HTTP-запросов.

        Set authorization token for API requests.

        Args:
            token: JWT токен авторизации / Authorization JWT token.
        """
        if not self._client:
            raise RuntimeError("SDK not initialized. Call initialize() first.")
        self._client.headers.update({"Authorization": f"Bearer {token}"})

    async def _refresh_access_token(self) -> None:
        """
        Обновляет пару токенов по stored refresh-токену (для авто-ретрая 401).

        Refreshes the token pair using the stored refresh token (for 401 auto-retry).
        """
        if self._client is None:
            raise RuntimeError("SDK not initialized. Call initialize() first.")
        if not self._refresh_token:
            raise OutdatedJWTError()
        response = await self.auth.refresh(
            RefreshTokenRequest(refresh_token=self._refresh_token)
        )
        self.set_auth_token(response.access_token)
        self._refresh_token = response.refresh_token

    async def close(self) -> None:
        """
        Закрывает HTTP-соединение.

        Close the client connection.

        Кешированные контроллеры сбрасываются, чтобы не держать stale-клиент.
        Cached controllers are dropped so they never hold a stale client.
        """
        if self._client:
            await self._client.aclose()
            self._client = None
        for attr_name in self._controller_names:
            setattr(self, attr_name, None)
        self._controller_names.clear()

    async def login(
        self, username: str, password: str, id_city: str | None = None
    ) -> str:
        """
        Авторизуется в журнале и возвращает токен доступа.

        Login to the journal and return access token.

        Args:
            username: Логин пользователя / Username.
            password: Пароль пользователя / Password.
            id_city: ID города (опционально) / City ID (optional).

        Returns:
            Токен доступа / Access token.

        Raises:
            ValueError: Если не удалось получить ключ приложения.
                      If application key could not be retrieved.
        """
        if self._client is None:
            raise RuntimeError("SDK not initialized. Call initialize() first.")
        app_key = ApplicationKey(
            JournalEndpoints.JOURNAL_BASE_URL.value,
            timeout=self._timeout,
            client=self._client,
        )
        app_token = await app_key.get_key()
        if not app_token:
            raise ValueError("Could not retrieve application key")

        auth_controller = self.auth
        login_data = LoginRequest(
            application_key=app_token,
            username=username,
            password=password,
            id_city=id_city,
        )
        response = await auth_controller.login(body=login_data)
        # Set auth token automatically after login
        self.set_auth_token(response.access_token)
        self._refresh_token = response.refresh_token
        # Cache session context (group/student) for controllers
        user_info = await self.user.get_personal_info()
        self._session.group_id = user_info.current_group_id
        self._session.student_id = user_info.student_id
        return response.access_token

    def _get_controller(self, attr_name: str, cls: type[T]) -> T:
        """
        Возвращает кешированный контроллер, создавая его при первом обращении.

        Returns a cached controller, creating it on first access.
        """
        if self._client is None:
            raise RuntimeError("SDK not initialized. Call initialize() first.")
        controller = getattr(self, attr_name)
        if controller is None:
            controller = cls(
                async_client=self._client,
                session=self._session,
                refresh_handler=self._refresh_access_token,
            )
            setattr(self, attr_name, controller)
            self._controller_names.add(attr_name)
        return cast(T, controller)

    @property
    def auth(self) -> AuthController:
        """
        Возвращает контроллер авторизации.

        Get auth controller.

        Returns:
            Экземпляр контроллера авторизации / Auth controller instance.
        """
        return self._get_controller("_auth_controller", AuthController)

    @property
    def user(self) -> UserInfoController:
        """
        Возвращает контроллер пользователей.

        Get user controller.

        Returns:
            Экземпляр контроллера пользователей / User controller instance.
        """
        return self._get_controller("_user_info_controller", UserInfoController)

    @property
    def attendance(self) -> AttendanceController:
        """
        Возвращает контроллер посещаемости.

        Get attendance controller.

        Returns:
            Экземпляр контроллера посещаемости / Attendance controller instance.
        """
        return self._get_controller("_attendance_controller", AttendanceController)

    @property
    def lesson_evaluation(self) -> LessonEvaluationController:
        """
        Возвращает контроллер оценок уроков.

        Get lesson evaluation controller.

        Returns:
            Экземпляр контроллера оценок уроков / Lesson evaluation controller instance.
        """
        return self._get_controller(
            "_lesson_evaluation_controller", LessonEvaluationController
        )

    @property
    def feedback(self) -> FeedbackController:
        """
        Возвращает контроллер отзывов.

        Get feedback controller.

        Returns:
            Экземпляр контроллера отзывов / Feedback controller instance.
        """
        return self._get_controller("_feedback_controller", FeedbackController)

    @property
    def grades(self) -> GradesController:
        """
        Возвращает контроллер оценок.

        Get grades controller.

        Returns:
            Экземпляр контроллера оценок / Grades controller instance.
        """
        return self._get_controller("_grades_controller", GradesController)

    @property
    def homework(self) -> HomeworkController:
        """
        Возвращает контроллер домашних заданий.

        Get homework controller.

        Returns:
            Экземпляр контроллера домашних заданий / Homework controller instance.
        """
        return self._get_controller("_homework_controller", HomeworkController)

    @property
    def leaderboard(self) -> LeaderboardController:
        """
        Возвращает контроллер таблицы лидеров.

        Get leaderboard controller.

        Returns:
            Экземпляр контроллера таблицы лидеров / Leaderboard controller instance.
        """
        return self._get_controller("_leaderboard_controller", LeaderboardController)

    @property
    def schedule(self) -> ScheduleController:
        """
        Возвращает контроллер расписания.

        Get schedule controller.

        Returns:
            Экземпляр контроллера расписания / Schedule controller instance.
        """
        return self._get_controller("_schedule_controller", ScheduleController)

    @property
    def dashboard(self) -> DashboardController:
        """
        Возвращает контроллер дашборда.

        Get dashboard controller.

        Returns:
            Экземпляр контроллера дашборда / Dashboard controller instance.
        """
        return self._get_controller("_dashboard_controller", DashboardController)

    @property
    def exams(self) -> ExamsController:
        """
        Возвращает контроллер экзаменов.

        Get exams controller.

        Returns:
            Экземпляр контроллера экзаменов / Exams controller instance.
        """
        return self._get_controller("_exams_controller", ExamsController)
