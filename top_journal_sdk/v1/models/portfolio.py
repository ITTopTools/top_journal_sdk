import datetime

from pydantic import HttpUrl

from top_journal_sdk._models import APIModel


class PortfolioResponse(APIModel):
    """Работа в портфолио.

    Portfolio entry.
    """

    id: int
    portfolio_title: str | None = None
    portfolio_description: str | None = None
    created_at: datetime.datetime | None = None
    teacher_name: str | None = None
    subject_name: str | None = None
    mark: int | None = None
    url: HttpUrl | None = None


class PortfoliosResponse(APIModel):
    portfolio_list: list[PortfolioResponse]


class DesignTeacherResponse(APIModel):
    """Преподаватель для дизайна портфолио.

    Portfolio design teacher.
    """

    id: int
    fio_teach: str | None = None


class DesignTeachersResponse(APIModel):
    design_teacher_list: list[DesignTeacherResponse]
