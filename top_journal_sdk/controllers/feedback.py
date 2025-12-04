from rapid_api_client import get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.feedback import ReviewResponse, ReviewsResponse
from top_journal_sdk.rapid.client import BaseController


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

                Список подробных отзывов с комплексной информацией о反馈.
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
