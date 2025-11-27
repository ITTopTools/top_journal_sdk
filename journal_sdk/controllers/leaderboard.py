from rapid_api_client import get

from journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from journal_sdk.models.leaderboard import (
    GroupLeaderboardResponse,
    GroupLeaderboardsResponse,
    StreamLeaderboardResponse,
    StreamLeaderboardsResponse,
)
from journal_sdk.rapid.client import BaseController


class LeaderboardController(BaseController):
    """
    Academic leaderboard controller.

    Handles retrieval of performance rankings for student groups and streams.
    Provides access to academic progress comparisons, achievement rankings,
    and competitive performance metrics across different cohorts.

    Контроллер рейтингов успеваемости.

    Обрабатывает получение рейтингов успеваемости для групп и потоков студентов.
    Предоставляет доступ к сравнению академической успеваемости, рейтингам достижений
    и метрикам конкурентоспособной успеваемости по разным группам.
    """

    @get(endpoints.GROUP_LEADERBOARD.value)
    async def get_group_leaderboard_list(self) -> list[GroupLeaderboardResponse]:
        """
        Get list of student group performance rankings.

        Retrieves ranking data for student groups based on academic performance,
        including group names, average scores, and position indicators
        for competitive analysis and progress tracking.

        Получить список рейтингов успеваемости студенческих групп.

        Возвращает данные рейтинга для студенческих групп на основе академической успеваемости,
        включая названия групп, средние баллы и индикаторы позиций
        для конкурентного анализа и отслеживания прогресса.

        Returns:
            list[GroupLeaderboardResponse]:
                List of group rankings with performance metrics and position data.

                Список рейтингов групп с метриками успеваемости и данными о позициях.
        """
        ...

    async def get_group_leaderboards(self) -> GroupLeaderboardsResponse:
        """
        Get complete group leaderboard information in response wrapper.

        Combines individual group rankings into a comprehensive object
        that provides organized access to all group performance data,
        including summary statistics and metadata for academic analysis.

        Получить полную информацию о рейтинге групп в обертке ответа.

        Комбинирует индивидуальные групповые рейтинги в комплексный объект,
        который предоставляет организованный доступ ко всем данным об успеваемости групп,
        включая сводную статистику и метаданные для академического анализа.

        Returns:
            GroupLeaderboardsResponse:
                Complete group leaderboard object with comprehensive data and statistics.

                Полный объект рейтинга групп с комплексными данными и статистикой.
        """
        return GroupLeaderboardsResponse(
            group_leaderboard_list=await self.get_group_leaderboard_list()
        )

    @get(endpoints.STREAM_LEADERBOARD.value)
    async def get_stream_leaderboard_list(self) -> list[StreamLeaderboardResponse]:
        """
        Get list of student stream performance rankings.

        Retrieves ranking data for student streams showing academic progress
        comparisons across larger cohorts, including stream identifiers,
        average performance metrics, and competitive positioning.

        Получить список рейтингов успеваемости студенческих потоков.

        Возвращает данные рейтинга для студенческих потоков, показывающие сравнение
        академической успеваемости по более крупным группам, включая идентификаторы потоков,
        средние метрики успеваемости и конкурентное позиционирование.

        Returns:
            list[StreamLeaderboardResponse]:
                List of stream rankings with cohort performance and position indicators.

                Список рейтингов потоков с метриками успеваемости групп и индикаторами позиций.
        """
        ...

    async def get_stream_leaderboards(self) -> StreamLeaderboardsResponse:
        """
        Get complete stream leaderboard information in response wrapper.

        Combines individual stream rankings into a comprehensive object
        that provides organized access to all stream performance data,
        including comparative analysis and cohort-based metrics.

        Получить полную информацию о рейтинге потоков в обертке ответа.

        Комбинирует индивидуальные рейтинг потоков в комплексный объект,
        который предоставляет организованный доступ ко всем данным об успеваемости потоков,
        включая сравнительный анализ и метрики, основанные на группах.

        Returns:
            StreamLeaderboardsResponse:
                Complete stream leaderboard object with cohort analysis and metrics.

                Полный объект рейтинга потоков с анализом групп и метриками.
        """
        return StreamLeaderboardsResponse(
            stream_leaderboard_list=await self.get_stream_leaderboard_list()
        )
