import pytest

from top_journal_sdk.v1.exceptions import DataNotFoundError
from top_journal_sdk.v1.models.homework import (
    HomeworkCounterResponse,
    HomeworkCounterType,
    HomeworksResponse,
)


def _response() -> HomeworksResponse:
    return HomeworksResponse(
        counter_list=[
            HomeworkCounterResponse(counter_type=HomeworkCounterType.TOTAL, counter=7),
            HomeworkCounterResponse(counter_type=HomeworkCounterType.OVERDUE, counter=2),
        ]
    )


def test_get_counter_by_enum() -> None:
    assert _response().get_counter(HomeworkCounterType.TOTAL) == 7


def test_get_counter_by_int() -> None:
    assert _response().get_counter(4) == 7


def test_counter_properties() -> None:
    response = _response()
    assert response.total == 7
    assert response.overdue == 2


def test_missing_counter_raises_domain_error() -> None:
    with pytest.raises(DataNotFoundError, match="Homework counter 1 not found"):
        _response().get_counter(HomeworkCounterType.CHECKED)


@pytest.mark.parametrize(
    "property_name,expected",
    [
        ("checked", 1),
        ("pending", 2),
        ("current", 3),
        ("deleted", 5),
    ],
)
def test_all_homework_counter_properties(property_name: str, expected: int) -> None:
    response = HomeworksResponse(
        counter_list=[
            HomeworkCounterResponse(counter_type=kind, counter=int(kind))
            for kind in HomeworkCounterType
        ]
    )
    assert getattr(response, property_name) == expected
