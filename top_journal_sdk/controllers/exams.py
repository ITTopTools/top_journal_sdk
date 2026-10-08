from rapid_api_client import get

from top_journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from top_journal_sdk.models.exams import (
    QuarterlyGradesResponse,
    StudentExamResponse,
    StudentExamsResponse,
)
from top_journal_sdk.rapid.client import BaseController, with_auth_refresh


class ExamsController(BaseController):
    """
    Student exams controller.

    Handles retrieval of exam results and quarterly grades.

    Контроллер экзаменов студента.

    Обрабатывает получение результатов экзаменов и четвертных оценок.
    """

    @with_auth_refresh
    @get(endpoints.STUDENT_EXAMS.value)
    async def get_student_exam_list(self) -> list[StudentExamResponse]:
        """
        Get student exams.

        Получить экзамены студента.

        Returns:
            list[StudentExamResponse]: Student exams / Экзамены студента.
        """
        ...

    async def get_student_exams(self) -> StudentExamsResponse:
        """
        Get student exams in response wrapper.

        Получить экзамены студента в обертке ответа.

        Returns:
            StudentExamsResponse: Exams object / Объект экзаменов.
        """
        return StudentExamsResponse(student_exam_list=await self.get_student_exam_list())

    @with_auth_refresh
    @get(endpoints.SCHOOL_QUARTERLY_GRADES.value)
    async def get_quarterly_grades(self) -> QuarterlyGradesResponse:
        """
        Get school quarterly grades.

        Получить четвертные оценки.

        Returns:
            QuarterlyGradesResponse: Quarterly grades / Четвертные оценки.
        """
        ...
