from abc import ABC, abstractmethod
from typing import List
from app.domain.models import Course
from app.domain.interfaces.repositories.Ibase_repository import IBaseRepository

class ICourseRepository(IBaseRepository[Course], ABC):
    @abstractmethod
    def get_by_instructor(self, instructor_id: int, organization_id: int) -> List[Course]:
        """Retrieve courses created by an instructor within a specific organization."""
        pass