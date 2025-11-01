from pydantic import BaseModel, Field
from typing import List
from enum import IntEnum

class HomeworkCounterType(IntEnum):
    OVERDUE = 0      # Просроченные
    CHECKED = 1      # Проверенные
    PENDING = 2      # На проверке
    CURRENT = 3      # Текущие
    TOTAL = 4        # Общее количество
    DELETED = 5      # Удалённые преподавателем


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
    hw_data: List[HomeworkCounter]
    
    def get_counter(self, counter_type: int | HomeworkCounterType) -> int:
        if isinstance(counter_type, HomeworkCounterType):
            counter_type = counter_type.value
        for counter in self.hw_data:
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
