import datetime

from pydantic import BaseModel, HttpUrl


class StudentExamResponse(BaseModel):
    """Экзамен студента.

    Student exam.
    """

    teacher: str | None = None
    mark: int | None = None
    mark_type: int | None = None
    # Через datetime.date: имя поля совпадает с именем типа date,
    # прямой импорт сделал бы аннотацию неразрешимой.
    date: datetime.date | None = None
    ex_file_name: str | None = None
    id_file: int | None = None
    exam_id: int | None = None
    file_path: HttpUrl | None = None
    comment_teach: str | None = None
    need_access: int | None = None
    need_access_stud: int | None = None
    comment_delete_file: str | None = None
    spec: str | None = None
    attestation_type: int | None = None
    subject_source: int | None = None
    subject_id: int | None = None


class StudentExamsResponse(BaseModel):
    student_exam_list: list[StudentExamResponse]


class QuarterlyGradeResponse(BaseModel):
    """Четвертная оценка.

    Quarterly grade.

    Точная форма пока не подтверждена: для тестового аккаунта эндпоинт
    возвращает пустой список. Модель будет уточнена по первому непустому образцу.
    """


class QuarterlyGradesResponse(BaseModel):
    """Четвертные оценки (форма ответа API — объект со списком).

    Quarterly grades (API responds with an object holding the list).
    """

    grades: list[QuarterlyGradeResponse]
