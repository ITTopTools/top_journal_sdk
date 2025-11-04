from pydantic import BaseModel, Field
from typing import List
from enum import IntEnum


class HomeworkCounterType(IntEnum):
    OVERDUE = 0
    CHECKED = 1
    PENDING = 2
    CURRENT = 3
    TOTAL = 4
    DELETED = 5


class HomeworkCounter(BaseModel):
    counter_type: int = Field(..., ge=0, le=5)
    counter: int = Field(..., ge=0)
    
    @property
    def type_name(self) -> str:
        names = {
            0: "Просроченные",
            1: "Проверенные", 
            2: "На проверке",
            3: "Текущие",
            4: "Общее количество",
            5: "Удалённые"
        }
        return names.get(self.counter_type, "Неизвестно")


class Homeworks(BaseModel):
    counters: List[HomeworkCounter]
    
    def get_counter(self, counter_type: int | HomeworkCounterType) -> int:
        if isinstance(counter_type, HomeworkCounterType):
            counter_type = counter_type.value
        
        for counter in self.counters:
            if counter.counter_type == counter_type:
                return counter.counter
        return 0
    
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
