from typing import Annotated

from httpx import Response
from rapid_api_client import PydanticBody, Query, get, post

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.feedback import (
    AcademyDayCommentRequest,
    AcademyDayResponse,
    ReviewResponse,
    ReviewsResponse,
    SetViewMaterialsRequest,
    SocialReviewResponse,
    SocialReviewsResponse,
)
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class FeedbackController(BaseController):
    """
    Student feedback controller.

    Handles retrieval of feedback and reviews about students.
    Provides access to teacher evaluations, peer reviews, and
    overall feedback history for academic performance assessment.

    Контроллер отзывов о студентах.

    Обрабатывает получение отзывов и оценок о студентах.
    Предоставляет доступ к оценкам преподавателей, отзывам одногруппников и
    общей истории отзывов для оценки академической успеваемости.
    """

    @with_auth_refresh
    @get(endpoints.STUDENT_REVIEWS.value)
    async def get_student_review_list(self) -> list[ReviewResponse]:
        """
        Get list of reviews and feedback about the student.

        Retrieves detailed reviews left by teachers, instructors, and other users
        about the student's academic performance, behavior, and overall progress.

        Получить список отзывов и обратной связи о студенте.

        Возвращает подробные отзывы, оставленные преподавателями, инструкторами и другими пользователями
        об академической успеваемости, поведении и общем прогрессе студента.

        Returns:
            list[ReviewResponse]:
                List of detailed reviews with comprehensive feedback information.

                Список подробных отзывов с комплексной информацией об обратной связи.
        """
        ...

    async def get_student_reviews(self) -> ReviewsResponse:
        """
        Get complete feedback information for the student in response wrapper.

        Combines individual reviews into a comprehensive object that provides
        an overview of all feedback received by the student, including ratings,
        comments, and evaluation history.

        Получить полную информацию об отзывах для студента в обертке ответа.

        Комбинирует индивидуальные отзывы в комплексный объект, который предоставляет
        обзор всей обратной связи, полученной студентом, включая оценки,
        комментарии и историю оценок.

        Returns:
            ReviewsResponse:
                Complete feedback object with all student reviews and evaluations.

                Полный объект обратной связи со всеми отзывами и оценками студента.
        """
        return ReviewsResponse(review_list=await self.get_student_review_list())

    @with_auth_refresh
    @get(endpoints.SOCIAL_REVIEW_LIST.value)
    async def get_social_review_list(self) -> list[SocialReviewResponse]:
        """
        Get list of social reviews.

        Получить список социальных отзывов.

        Returns:
            list[SocialReviewResponse]: Social reviews / Социальные отзывы.
        """
        ...

    async def get_social_reviews(self) -> SocialReviewsResponse:
        """
        Get social reviews in response wrapper.

        Получить социальные отзывы в обертке ответа.

        Returns:
            SocialReviewsResponse: Social reviews object / Объект отзывов.
        """
        return SocialReviewsResponse(
            social_review_list=await self.get_social_review_list()
        )

    @with_auth_refresh
    @get(endpoints.REVIEWS_INSTRUCTION.value)
    async def get_reviews_instruction(self) -> str:
        """
        Get reviews instruction text.

        Получить текст инструкции по отзывам.

        Returns:
            str: Instruction text / Текст инструкции.
        """
        ...

    @with_auth_refresh
    @post(endpoints.SOCIAL_REVIEW_SCREEN.value, raise_for_status=True)
    async def post_social_review_screen_response(
        self,
        body: Annotated[SocialReviewResponse, PydanticBody()],  # pyright: ignore[reportUnusedParameter]
    ) -> Response:
        """
        Submit a social review screenshot (raw response).

        Отправить скриншот отзыва (сырой ответ).
        """
        ...

    async def post_social_review_screen(
        self, review: SocialReviewResponse
    ) -> bool:
        """
        Submit a social review screenshot.

        Отправить скриншот социального отзыва.

        Args:
            review: Social review with screenshot / Отзыв со скриншотом.

        Returns:
            True on success (raises on HTTP errors) / True при успехе.
        """
        response = await self.post_social_review_screen_response(review)
        return response.is_success

    @with_auth_refresh
    @get(endpoints.ACADEMY_DAY_EVALUATE.value)
    async def get_academy_day_list(
        self,
        evaluation: Annotated[int, Query()],  # pyright: ignore[reportUnusedParameter]
    ) -> list[AcademyDayResponse]:
        """
        Get academy day evaluation form.

        Получить форму оценки академического дня.

        Args:
            evaluation: Academy day evaluation ID / ID оценки академического дня.

        Returns:
            list[AcademyDayResponse]: Evaluation form / Форма оценки.
        """
        ...

    async def get_academy_day(self, evaluation: int) -> AcademyDayResponse | None:
        """
        Get academy day evaluation form (first entry).

        Получить форму оценки академического дня (первая запись).

        Args:
            evaluation: Academy day evaluation ID / ID оценки академического дня.

        Returns:
            AcademyDayResponse | None: Form or None / Форма или None.
        """
        entries = await self.get_academy_day_list(evaluation)
        return entries[0] if entries else None

    @with_auth_refresh
    @post(endpoints.ACADEMY_DAY_COMMENT.value, raise_for_status=True)
    async def post_academy_day_comment_response(
        self,
        body: Annotated[AcademyDayCommentRequest, PydanticBody()],  # pyright: ignore[reportUnusedParameter]
    ) -> Response:
        """
        Submit an academy day comment (raw response).

        Отправить комментарий к академическому дню (сырой ответ).
        """
        ...

    async def post_academy_day_comment(
        self, evaluation_id: int, message: str
    ) -> bool:
        """
        Submit an academy day comment.

        Отправить комментарий к академическому дню.

        Args:
            evaluation_id: Academy day evaluation ID / ID оценки.
            message: Comment text / Текст комментария.

        Returns:
            True on success (raises on HTTP errors) / True при успехе.
        """
        response = await self.post_academy_day_comment_response(
            AcademyDayCommentRequest(id=evaluation_id, message=message)
        )
        return response.is_success

    @with_auth_refresh
    @post(endpoints.SET_VIEW_MATERIALS.value, raise_for_status=True)
    async def post_set_view_materials_response(
        self,
        body: Annotated[SetViewMaterialsRequest, PydanticBody()],  # pyright: ignore[reportUnusedParameter]
    ) -> Response:
        """
        Mark a library material as viewed (raw response).

        Отметить материал библиотеки просмотренным (сырой ответ).
        """
        ...

    async def post_set_view_materials(
        self, material_type: int, material_ids: list[int]
    ) -> bool:
        """
        Mark library materials as viewed.

        Отметить материалы библиотеки просмотренными.

        Args:
            material_type: Material type / Тип материала.
            material_ids: Viewed material IDs / ID просмотренных материалов.

        Returns:
            True on success (raises on HTTP errors) / True при успехе.
        """
        response = await self.post_set_view_materials_response(
            SetViewMaterialsRequest(type=material_type, materials=material_ids)
        )
        return response.is_success
