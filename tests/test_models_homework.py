import pytest

from top_journal_sdk.exceptions import DataNotFoundError
from top_journal_sdk.models.homework import (
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
