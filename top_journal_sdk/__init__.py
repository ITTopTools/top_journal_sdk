from httpx import AsyncClient

from top_journal_sdk.controllers import (
    AttendanceController,
    AuthController,
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
from top_journal_sdk.models.auth import LoginRequest
from top_journal_sdk.utils.app_key import ApplicationKey


class TopJournalSDK:
    """
    Основной класс SDK для взаимодействия с Top Academy Journal API.

    Main SDK class for interacting with Top Academy Journal API.
    """

    def __init__(self):
        """
        Инициализирует SDK с пустыми значениями контроллеров.

        Initialize the SDK with empty controller values.
        """
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
        """
        self._client = AsyncClient(
            base_url=JournalEndpoints.API_BASE_URL.value, follow_redirects=True
        )
        headers: dict[str, str] = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": JournalHeaders.ORIGIN.value,
            "Referer": JournalHeaders.REFERER.value,
            "User-Agent": JournalHeaders.USER_AGENT.value,
        }
        self._client.headers.update(headers)

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

    async def close(self) -> None:
        """
        Закрывает HTTP-соединение.

        Close the client connection.
        """
        if self._client:
            await self._client.aclose()
            self._client = None

    async def login(self, username: str, password: str) -> str:
        """
        Авторизуется в журнале и возвращает токен доступа.

        Login to the journal and return access token.

        Args:
            username: Логин пользователя / Username.
            password: Пароль пользователя / Password.

        Returns:
            Токен доступа / Access token.

        Raises:
            ValueError: Если не удалось получить ключ приложения.
                      If application key could not be retrieved.
        """
        app_key = ApplicationKey(JournalEndpoints.JOURNAL_BASE_URL.value)
        app_token = await app_key.get_key()
        if not app_token:
            raise ValueError("Could not retrieve application key")

        auth_controller = AuthController(async_client=self._client)
        login_data = LoginRequest(
            application_key=app_token, username=username, password=password
        )
        response = await auth_controller.login(body=login_data)
        # Set auth token automatically after login
        self.set_auth_token(response.access_token)
        return response.access_token

    @property
    def auth(self) -> AuthController:
        """
        Возвращает контроллер авторизации.

        Get auth controller.

        Returns:
            Экземпляр контроллера авторизации / Auth controller instance.
        """
        if not self._auth_controller:
            if not self._client:
                raise RuntimeError("SDK not initialized. Call initialize() first.")
            self._auth_controller = AuthController(async_client=self._client)
        return self._auth_controller

    @property
    def user(self) -> UserInfoController:
        """
        Возвращает контроллер пользователей.

        Get user controller.

        Returns:
            Экземпляр контроллера пользователей / User controller instance.
        """
        if not self._user_info_controller:
            if not self._client:
                raise RuntimeError("SDK not initialized. Call initialize() first.")
            self._user_info_controller = UserInfoController(async_client=self._client)
        return self._user_info_controller

    @property
    def attendance(self) -> AttendanceController:
        """
        Возвращает контроллер посещаемости.

        Get attendance controller.

        Returns:
            Экземпляр контроллера посещаемости / Attendance controller instance.
        """
        if not self._attendance_controller:
            if not self._client:
                raise RuntimeError("SDK not initialized. Call initialize() first.")
            self._attendance_controller = AttendanceController(
                async_client=self._client
            )
        return self._attendance_controller

    @property
    def lesson_evaluation(self) -> LessonEvaluationController:
        """
        Возвращает контроллер оценок уроков.

        Get lesson evaluation controller.

        Returns:
            Экземпляр контроллера оценок уроков / Lesson evaluation controller instance.
        """
        if not self._lesson_evaluation_controller:
            if not self._client:
                raise RuntimeError("SDK not initialized. Call initialize() first.")
            self._lesson_evaluation_controller = LessonEvaluationController(
                async_client=self._client
            )
        return self._lesson_evaluation_controller

    @property
    def feedback(self) -> FeedbackController:
        """
        Возвращает контроллер отзывов.

        Get feedback controller.

        Returns:
            Экземпляр контроллера отзывов / Feedback controller instance.
        """
        if not self._feedback_controller:
            if not self._client:
                raise RuntimeError("SDK not initialized. Call initialize() first.")
            self._feedback_controller = FeedbackController(async_client=self._client)
        return self._feedback_controller

    @property
    def grades(self) -> GradesController:
        """
        Возвращает контроллер оценок.

        Get grades controller.

        Returns:
            Экземпляр контроллера оценок / Grades controller instance.
        """
        if not self._grades_controller:
            if not self._client:
                raise RuntimeError("SDK not initialized. Call initialize() first.")
            self._grades_controller = GradesController(async_client=self._client)
        return self._grades_controller

    @property
    def homework(self) -> HomeworkController:
        """
        Возвращает контроллер домашних заданий.

        Get homework controller.

        Returns:
            Экземпляр контроллера домашних заданий / Homework controller instance.
        """
        if not self._homework_controller:
            if not self._client:
                raise RuntimeError("SDK not initialized. Call initialize() first.")
            self._homework_controller = HomeworkController(async_client=self._client)
        return self._homework_controller

    @property
    def leaderboard(self) -> LeaderboardController:
        """
        Возвращает контроллер таблицы лидеров.

        Get leaderboard controller.

        Returns:
            Экземпляр контроллера таблицы лидеров / Leaderboard controller instance.
        """
        if not self._leaderboard_controller:
            if not self._client:
                raise RuntimeError("SDK not initialized. Call initialize() first.")
            self._leaderboard_controller = LeaderboardController(
                async_client=self._client
            )
        return self._leaderboard_controller

    @property
    def schedule(self) -> ScheduleController:
        """
        Возвращает контроллер расписания.

        Get schedule controller.

        Returns:
            Экземпляр контроллера расписания / Schedule controller instance.
        """
        if not self._schedule_controller:
            if not self._client:
                raise RuntimeError("SDK not initialized. Call initialize() first.")
            self._schedule_controller = ScheduleController(async_client=self._client)
        return self._schedule_controller
