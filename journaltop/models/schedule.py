from datetime import date, time
from typing import List, Optional

from pydantic import BaseModel, Field

class Lesson(BaseModel):
    """One lesson"""
    date: date
    lesson: int = Field(..., ge=0, le=8)
    started_at: time
    finished_at: time
    teacher_name: str
    subject_name: str
    room_name: str


class Schedule(BaseModel):
    """
    Full leasson's object
    
    How to use:
        from raw to object: 
        schedule = Schedule(leasons=<data_list>)
        
        get data:
        print(schedule.lesson(1).started_at)
        print(schedule.lesson(1).finished_at)
        print(schedule.lesson(1).teacher_name)
        print(schedule.lesson(2).subject_name)
        print(schedule.lesson(3).room_name)
    
    """
    lessons: List[Lesson]
    
    def lesson(self, number: int) -> Optional[Lesson]:
        """Get lesson"""
        for lesson in self.lessons:
            if lesson.lesson == number:
                return lesson
        return None
