from typing import Annotated, Literal

from rapid_api_client import PydanticBody, Query, get, post

from journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from journal_sdk.models.evaluation import (
    EvaluationRequest,
    EvaluationResponse,
    EvaluationsResponse,
    EvaluationTagResponse,
    EvaluationTagsResponse,
)
from journal_sdk.rapid.client import BaseController


class LessonEvaluationController(BaseController):
    """
    Lesson evaluation controller.

    Handles student evaluation of completed lessons and classes.
    Provides access to evaluation forms, lesson tags, and submission
    of ratings and feedback for academic improvement.

    Контроллер оценки уроков.

    Обрабатывает оценку пройденных уроков и занятий студентами.
    Предоставляет доступ к формам оценки, тегам уроков и отправке
    оценок и отзывов для академического улучшения.
    """

    @get(endpoints.EVALUATION_LESSON_TAGS.value)
    async def get_evaluation_lesson_tag_list(
        self,
        type: Annotated[Literal["evaluation_lesson", "evaluation_lesson_teach"], Query()],  # pyright: ignore[reportUnusedParameter]
    ) -> list[EvaluationTagResponse]:
        """
        Get list of evaluation tags for lesson assessment.

        Retrieves categorized tags that can be used for evaluating
        different aspects of lessons, such as teaching quality,
        content relevance, and learning effectiveness.

        Получить список тегов оценки для оценки уроков.

        Возвращает категоризированные теги, которые могут использоваться для оценки
        разных аспектов уроков, таких как качество преподавания,
        актуальность содержания и эффективность обучения.

        Args:
            type:
                Type of evaluation tags to retrieve (lesson or teaching evaluation).

                Тип тегов оценки для получения (оценка урока или преподавания).

        Returns:
            list[EvaluationTagResponse]:
                List of evaluation tags categorized by assessment criteria.

                Список тегов оценки, категоризированных по критериям оценки.
        """
        ...

    async def get_evaluation_lesson_tags(
        self, type: Literal["evaluation_lesson", "evaluation_lesson_teach"]
    ) -> EvaluationTagsResponse:
        """
        Get evaluation tags in comprehensive response wrapper.

        Combines evaluation tags into a structured response object
        that provides organized access to all available assessment
        criteria for lesson evaluation.

        Получить теги оценки в комплексной обертке ответа.

        Комбинирует теги оценки в структурированный объект ответа,
        который предоставляет организованный доступ ко всем доступным критериям
        оценки для оценки уроков.

        Args:
            type:
                Type of evaluation (lesson or teaching focused).

                Тип оценки (ориентированной на урок или преподавание).

        Returns:
            EvaluationTagsResponse:
                Structured response containing all evaluation tags and metadata.

                Структурированный ответ, содержащий все теги оценки и метаданные.
        """
        return EvaluationTagsResponse(
            evaluation_tags=await self.get_evaluation_lesson_tag_list(type)
        )

    @get(endpoints.LESSONS_TO_EVALUATE.value)
    async def get_evaluation_lesson_list(self) -> list[EvaluationResponse]:
        """
        Get list of lessons available for student evaluation.

        Retrieves all completed lessons that are currently available
        for student feedback and rating, including lesson details
        and evaluation status.

        Получить список уроков, доступных для оценки студентами.

        Возвращает все пройденные уроки, которые в настоящее время доступны
        для обратной связи и оценки студентами, включая детали уроков
        и статус оценки.

        Returns:
            list[EvaluationResponse]:
                List of lessons ready for evaluation with complete information.

                Список уроков, готовых к оценке, с полной информацией.
        """
        ...

    async def get_evaluation_lessons(self) -> EvaluationsResponse:
        """
        Get complete evaluation lessons information in response wrapper.

        Combines individual lesson evaluations into a comprehensive object
        that provides an overview of all available lessons for assessment,
        including evaluation deadlines and submission status.

        Получить полную информацию об уроках для оценки в обертке ответа.

        Комбинирует индивидуальные оценки уроков в комплексный объект,
        который предоставляет обзор всех доступных уроков для оценки,
        включая сроки оценки и статус отправки.

        Returns:
            EvaluationsResponse:
                Complete evaluation lessons object with metadata and status.

                Полный объект уроков для оценки с метаданными и статусом.
        """
        return EvaluationsResponse(evaluation_list=await self.get_evaluation_lesson_list())

    @post(endpoints.SUBMIT_EVALUATION_LESSONS.value)
    async def submit_evaluate_lesson(
        self,
        body: Annotated[EvaluationRequest, PydanticBody()],  # pyright: ignore[reportUnusedParameter]
    ) -> None:
        """
        Submit evaluation and feedback for a completed lesson.

        Sends student rating and comments for a specific lesson,
        including evaluation scores, written feedback, and optional
        tags for comprehensive lesson assessment.

        Отправить оценку и отзыв по пройденному уроку.

        Отправляется оценка и комментарии студента по конкретному уроку,
        включая баллы оценки, письменный отзыв и опциональные
        теги для комплексной оценки урока.

        Args:
            body:
                Evaluation data including rating, comments, and tags.

                Данные оценки, включая рейтинг, комментарии и теги.

        Returns:
            None:
                Successful submission confirmation (raises exception on failure).

                Подтверждение успешной отправки (вызывает исключение при неудаче).
        """
        ...
