from enum import IntEnum

from pydantic import BaseModel

from top_journal_sdk.exceptions import DataNotFoundError


class HomeworkCounterType(IntEnum):
    OVERDUE = 0
    CHECKED = 1
    PENDING = 2
    CURRENT = 3
    TOTAL = 4
    DELETED = 5


class HomeworkCounterResponse(BaseModel):
    counter_type: HomeworkCounterType
    counter: int


class HomeworksResponse(BaseModel):
    counter_list: list[HomeworkCounterResponse]

    def get_counter(self, counter_type: int | HomeworkCounterType) -> int:
        if isinstance(counter_type, HomeworkCounterType):
            counter_type = counter_type.value

        for counter in self.counter_list:
            if counter.counter_type == counter_type:
                return counter.counter
        raise DataNotFoundError(message=f"Homework counter {counter_type} not found")

    @property
    def overdue(self) -> int:
        return self.get_counter(HomeworkCounterType.OVERDUE)

    @property
    def checked(self) -> int:
        return self.get_counter(HomeworkCounterType.CHECKED)

    @property
    def pending(self) -> int:
        return self.get_counter(HomeworkCounterType.PENDING)

    @property
    def current(self) -> int:
        return self.get_counter(HomeworkCounterType.CURRENT)

    @property
    def total(self) -> int:
        return self.get_counter(HomeworkCounterType.TOTAL)

    @property
    def deleted(self) -> int:
        return self.get_counter(HomeworkCounterType.DELETED)
