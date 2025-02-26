from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models import Enrollment
from app.domain.interfaces.repositories.Ibase_repository import BaseRepository

class IEnrollmentRepository(BaseRepository[Enrollment], ABC):
    """Interface for enrollment-specific database operations."""

    @abstractmethod
    def get_by_user_and_course(self, user_id: int, course_id: int) -> Optional[Enrollment]:
        pass
