"""Unit-тесты моделей Волны 1 на синтетических payload (без сети)."""

from datetime import date, datetime

from top_journal_sdk.models.dashboard import (
    AcademicProgressResponse,
    AttendanceStatisticResponse,
    LeaderPointsResponse,
    PageCounterResponse,
)
from top_journal_sdk.models.exams import StudentExamResponse
from top_journal_sdk.models.grades import ClassAttendanceGradeResponse
from top_journal_sdk.models.homework import (
    GroupHistoryResponse,
    HomeworkListItemResponse,
    HomeworkTagResponse,
)
from top_journal_sdk.models.schedule import MonthEventResponse


def test_homework_list_item_full() -> None:
    item = HomeworkListItemResponse.model_validate(
        {
            "id": 1,
            "id_spec": 2,
            "subject_source": 1,
            "subject_id": 3,
            "id_teach": 4,
            "id_group": 9,
            "fio_teach": "Teacher",
            "theme": "Theme",
            "completion_time": "2026-10-08",
            "creation_time": "2026-09-28",
            "overdue_time": None,
            "filename": None,
            "file_path": "https://fs.top-academy.ru/x",
            "comment": "",
            "name_spec": "Spec",
            "status": 1,
            "common_status": None,
            "homework_stud": {"id": 5, "mark": 12},
            "homework_comment": {"date_updated": "2026-09-28 10:17:54"},
            "cover_image": None,
        }
    )
    assert item.id == 1
    assert item.completion_time == date(2026, 10, 8)
    assert item.homework_stud is not None and item.homework_stud.mark == 12
    assert item.homework_comment is not None
    assert item.homework_comment.date_updated == datetime(2026, 9, 28, 10, 17, 54)


def test_homework_list_item_minimal() -> None:
    item = HomeworkListItemResponse.model_validate(
        {
            "id": 1,
            "id_spec": 2,
            "subject_source": 1,
            "subject_id": 3,
            "id_teach": 4,
            "id_group": 9,
        }
    )
    assert item.homework_stud is None
    assert item.status is None


def test_homework_tag() -> None:
    tag = HomeworkTagResponse.model_validate(
        {"id": 1, "translate_key": "everything_is_cool_tag", "type": "evaluation_homework"}
    )
    assert tag.translate_key == "everything_is_cool_tag"


def test_group_history() -> None:
    history = GroupHistoryResponse.model_validate(
        {
            "specs": [{"id": 1, "name": "Math", "short_name": "M"}],
            "id": 9,
            "name": "9/2-25/1",
        }
    )
    assert history.specs[0].name == "Math"


def test_academic_performance_aliases() -> None:
    perf = AcademicProgressResponse.model_validate(
        {
            "diffMonth": 1,
            "totalMonth": 80,
            "totalAllTime": 75.5,
            "maxAllowedPoint": 100,
            "progress": {"homework": 90.0, "total": 80.0},
        }
    )
    assert perf.diff_month == 1
    assert perf.progress["total"] == 80.0


def test_attendance_statistic_aliases() -> None:
    stat = AttendanceStatisticResponse.model_validate(
        {
            "diffMonth": 0,
            "diffWeek": 1,
            "statMonth": 95,
            "statWeek": 100,
            "statTotal": 97,
        }
    )
    assert stat.stat_total == 97


def test_leader_points_nullable_total() -> None:
    points = LeaderPointsResponse.model_validate(
        {
            "totalCount": None,
            "studentPosition": 5,
            "weekDiff": 1,
            "monthDiff": -2,
        }
    )
    assert points.total_count is None
    assert points.student_position == 5


def test_page_counter() -> None:
    counter = PageCounterResponse.model_validate({"counter_type": 3, "counter": 12})
    assert counter.counter == 12


def test_student_exam() -> None:
    exam = StudentExamResponse.model_validate(
        {
            "teacher": "Teacher",
            "mark": 5,
            "mark_type": 1,
            "date": "2026-07-28",
            "ex_file_name": None,
            "id_file": 7,
            "exam_id": 8,
            "file_path": None,
            "comment_teach": None,
            "need_access": 0,
            "need_access_stud": None,
            "comment_delete_file": None,
            "spec": "Math",
            "attestation_type": 2,
            "subject_source": 1,
            "subject_id": 3,
        }
    )
    assert exam.mark == 5
    assert exam.date == date(2026, 7, 28)


def test_month_event_unconfirmed_shape() -> None:
    assert MonthEventResponse.model_validate({}) is not None


def test_class_attendance_grade_nullable_lesson() -> None:
    # Live: у части записей lesson_number=null (регрессия sweep Волны 4).
    grade = ClassAttendanceGradeResponse.model_validate(
        {
            "date_visit": "2026-10-07",
            "lesson_number": None,
            "status_was": None,
            "spec_id": 81,
            "teacher_name": "Teacher",
            "spec_name": "Spec",
            "lesson_theme": "Theme",
            "control_work_mark": None,
            "home_work_mark": None,
            "lab_work_mark": None,
            "class_work_mark": None,
            "practical_work_mark": None,
            "final_work_mark": None,
            "final_work_mark_type": None,
        }
    )
    assert grade.lesson_number is None
