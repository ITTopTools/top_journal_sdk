from datetime import datetime

from pydantic import BaseModel


class ReviewResponse(BaseModel):
    date: datetime
    message: str
    spec: str
    full_spec: str
    teacher: str


class ReviewsResponse(BaseModel):
    review_list: list[ReviewResponse]


class SocialReviewResponse(BaseModel):
    """Социальный отзыв (ссылка студента на внешний отзыв).

    Social review (student link to an external review).
    """

    status: int | None = None
    social_id: int
    link_id: int | None = None
    link: str | None = None
    screen_shot: str | None = None
    review_id: int | None = None
    comment: str | None = None
    teach_name: str | None = None
    updated_at: datetime | None = None
    is_visibility: bool | None = None


class SocialReviewsResponse(BaseModel):
    social_review_list: list[SocialReviewResponse]


class AcademyDayResponse(BaseModel):
    """Форма оценки академического дня.

    Academy day evaluation form.
    """

    id: int | None = None
    id_city: int | None = None
    evaluation: int | None = None
    default_lang: str | None = None


class AcademyDayCommentRequest(BaseModel):
    """Комментарий к академическому дню.

    Academy day comment.

    Поля по форме фронта: идентификатор оценки и текст сообщения.
    """

    id: int
    message: str


class SetViewMaterialsRequest(BaseModel):
    """Отметка просмотра материалов библиотеки.

    Library materials view marking.

    Форма фронта: ViewLibraryForm(type, materials) — тип и список ID.
    """

    type: int
    materials: list[int]
