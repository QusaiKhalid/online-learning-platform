from abc import ABC, abstractmethod
from typing import List
from app.domain.models import Course
from app.domain.interfaces.repositories.Ibase_repository import IBaseRepository

class ICourseRepository(IBaseRepository[Course], ABC):
    """Interface for course-specific database operations."""

    @abstractmethod
    def get_by_instructor(self, instructor_id: int) -> List[Course]:
        pass
