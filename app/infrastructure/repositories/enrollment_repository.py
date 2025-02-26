from domain.interfaces.repositories.Ienrollment_repository import IEnrollmentRepository
from domain.models import Enrollment
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from typing import Optional

class EnrollmentRepository(BaseRepository[Enrollment], IEnrollmentRepository):
    """Enrollment repository implementation using BaseRepository."""

    def __init__(self, db_session: Session):
        super().__init__(db_session, Enrollment)

    def get_by_user_and_course(self, user_id: int, course_id: int) -> Optional[Enrollment]:
        """Fetch enrollment record by user ID and course ID."""
        return self.db_session.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        ).first()  # Use .first() to get the first match or None if not found
