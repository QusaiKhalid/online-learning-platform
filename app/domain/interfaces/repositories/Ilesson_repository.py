from abc import ABC, abstractmethod
from typing import List
from app.domain.models import Lesson
from app.domain.interfaces.repositories.Ibase_repository import BaseRepository

class ILessonRepository(BaseRepository[Lesson], ABC):
    """Interface for lesson-specific database operations."""

    @abstractmethod
    def get_by_course(self, course_id: int) -> List[Lesson]:
        pass
