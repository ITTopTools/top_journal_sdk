from enum import IntEnum

from pydantic import BaseModel


class HomeworkCounterType(IntEnum):
    OVERDUE = 0
    CHECKED = 1
    PENDING = 2
    CURRENT = 3
    TOTAL = 4
    DELETED = 5


class HomeworkCounter(BaseModel):
    counter_type: HomeworkCounterType
    counter: int


class Homeworks(BaseModel):
    counters: list[HomeworkCounter]

    def get_counter(self, counter_type: int | HomeworkCounterType) -> int | None:
        if isinstance(counter_type, HomeworkCounterType):
            counter_type = counter_type.value

        for counter in self.counters:
            if counter.counter_type == counter_type:
                return counter.counter
        raise IndexError

    @property
    def overdue(self) -> int | None:
        return self.get_counter(HomeworkCounterType.OVERDUE)

    @property
    def checked(self) -> int | None:
        return self.get_counter(HomeworkCounterType.CHECKED)

    @property
    def pending(self) -> int | None:
        return self.get_counter(HomeworkCounterType.PENDING)

    @property
    def current(self) -> int | None:
        return self.get_counter(HomeworkCounterType.CURRENT)

    @property
    def total(self) -> int | None:
        return self.get_counter(HomeworkCounterType.TOTAL)

    @property
    def deleted(self) -> int | None:
        return self.get_counter(HomeworkCounterType.DELETED)
