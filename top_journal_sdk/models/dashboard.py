import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChartPointResponse(BaseModel):
    """Точка графика прогресса.

    Progress chart point.

    Имена JSON-ключей точек не подтверждены сэмплами (для тестового аккаунта
    графики пусты), поэтому поля опциональны и заполнятся при уточнении формы.
    """

    chart_date: str | None = None
    chart_value: float | None = None
    previous_chart_value: float | None = None


class ProgressChartResponse(BaseModel):
    """График прогресса.

    Progress chart.
    """

    chart_type: int
    chart_models: list[ChartPointResponse]


class ProgressChartsResponse(BaseModel):
    progress_chart_list: list[ProgressChartResponse]


class FutureExamResponse(BaseModel):
    """Будущий экзамен.

    Future exam.

    Точная форма пока не подтверждена: для тестового аккаунта эндпоинт
    возвращает пустой список. Модель будет уточнена по первому непустому образцу.
    """


class FutureExamsResponse(BaseModel):
    future_exam_list: list[FutureExamResponse]


class AcademicProgressResponse(BaseModel):
    """Детализация академической успеваемости.

    Academic performance breakdown.
    """

    model_config = ConfigDict(populate_by_name=True)

    diff_month: int = Field(alias="diffMonth")
    total_month: int = Field(alias="totalMonth")
    total_all_time: float = Field(alias="totalAllTime")
    max_allowed_point: int = Field(alias="maxAllowedPoint")
    progress: dict[str, float]


class ActivityResponse(BaseModel):
    """Запись активности студента.

    Student activity entry.
    """

    date: datetime.datetime | None = None
    action: int | None = None
    current_point: int | None = None
    point_types_id: int | None = None
    point_types_name: str | None = None
    achievements_id: int | None = None
    achievements_name: str | None = None
    achievements_type: int | None = None
    badge: int | None = None
    old_competition: bool | None = None


class ActivitiesResponse(BaseModel):
    activity_list: list[ActivityResponse]


class AttendanceStatisticResponse(BaseModel):
    """Статистика посещаемости.

    Attendance statistic.
    """

    model_config = ConfigDict(populate_by_name=True)

    diff_month: int = Field(alias="diffMonth")
    diff_week: int = Field(alias="diffWeek")
    stat_month: int = Field(alias="statMonth")
    stat_week: int = Field(alias="statWeek")
    stat_total: int = Field(alias="statTotal")


class LeaderPointsResponse(BaseModel):
    """Баллы рейтинга (группа/поток): позиция студента и динамика.

    Leaderboard points (group/stream): student position and deltas.
    """

    model_config = ConfigDict(populate_by_name=True)

    total_count: int | None = Field(default=None, alias="totalCount")
    student_position: int = Field(alias="studentPosition")
    week_diff: int = Field(alias="weekDiff")
    month_diff: int = Field(alias="monthDiff")


class PageCounterResponse(BaseModel):
    """Счетчик страниц.

    Page counter.
    """

    counter_type: int
    counter: int


class PageCountersResponse(BaseModel):
    page_counter_list: list[PageCounterResponse]
