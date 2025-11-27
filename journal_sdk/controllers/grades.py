from rapid_api_client import get

from journal_sdk.enums.endpoints import JournalEndpoints as endpoints
from journal_sdk.models.grades import (
    ClassAttendanceGradeResponse,
    ClassAttendanceGradesResponse,
    GradeResponse,
    GradesResponse,
)
from journal_sdk.rapid.client import BaseController


class GradesController(BaseController):
    """
    Academic grades controller.

    Handles retrieval of student grades and academic performance data.
    Provides access to average grades, class attendance grades, and
    overall academic progress information.

    Контроллер оценок студентов.

    Обрабатывает получение оценок студентов и данных об академической успеваемости.
    Предоставляет доступ к средним оценкам, оценкам за посещаемость и
    общей информации об академическом прогрессе.
    """

    @get(endpoints.AVERAGE_GRADE.value)
    async def get_average_grade_list(self) -> list[GradeResponse]:
        """
        Get list of student's average grades by subjects.

        Retrieves calculated average grades for each subject,
        representing the student's academic performance across different disciplines.

        Получить список средних оценок студента по предметам.

        Возвращает рассчитанные средние оценки по каждому предмету,
        представляющие академическую успеваемость студента по разным дисциплинам.

        Returns:
            list[GradeResponse]:
                List of objects with information about average grades by subjects.

                Список объектов с информацией о средних оценках по предметам.
        """
        ...

    async def get_average_grades(self) -> GradesResponse:
        """
        Get student's average grades in a comprehensive response wrapper.

        Combines individual subject grades into a complete response object
        that provides an overview of the student's academic performance.

        Получить средние оценки студента в комплексной обертке ответа.

        Комбинирует индивидуальные оценки по предметам в полный объект ответа,
        который предоставляет обзор академической успеваемости студента.

        Returns:
            GradesResponse:
                Object with comprehensive student's average grades information.

                Объект с комплексной информацией о средних оценках студента.
        """
        return GradesResponse(grade_list=await self.get_average_grade_list())

    @get(endpoints.CLASS_ATTENDANCE_GRADES.value)
    async def get_class_attendance_grade_list(self) -> list[ClassAttendanceGradeResponse]:
        """
        Get list of grades assigned for class attendance evaluation.

        Retrieves specific grades that have been given based on student
        attendance and participation in classes, separate from academic grades.

        Получить список оценок, выставленных за посещаемость занятий.

        Возвращает конкретные оценки, которые были выставлены на основе
        посещаемости и участия студента на занятиях, отдельно от академических оценок.

        Returns:
            list[ClassAttendanceGradeResponse]:
                List of objects with information about attendance-based grades.

                Список объектов с информацией об оценках, основанных на посещаемости.
        """
        ...

    async def get_class_attendance_grades(self) -> ClassAttendanceGradesResponse:
        """
        Get attendance grades in a comprehensive response wrapper.

        Combines individual attendance grades into a complete response object
        that provides an overview of student's attendance-based evaluation.

        Получить оценки за посещаемость в комплексной обертке ответа.

        Комбинирует индивидуальные оценки за посещаемость в полный объект ответа,
        который предоставляет обзор оценки студента на основе посещаемости.

        Returns:
            ClassAttendanceGradesResponse:
                Object with comprehensive attendance grades information.

                Объект с комплексной информацией об оценках за посещаемость.
        """
        return ClassAttendanceGradesResponse(
            class_attendance_grade_list=await self.get_class_attendance_grade_list()
        )
