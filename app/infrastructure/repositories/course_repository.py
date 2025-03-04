from domain.interfaces.repositories.Icourse_repository import ICourseRepository
from domain.models import Course
from app.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from typing import List

class CourseRepository(BaseRepository[Course], ICourseRepository):
    """Course repository implementation using BaseRepository."""

    def __init__(self, db_session: Session):
        super().__init__(db_session, Course)

    def get_by_instructor(self, instructor_id: int) -> List[Course]:
        """Fetch all courses assigned to a specific instructor."""
        return self.db_session.query(Course).filter(Course.instructor_id == instructor_id, Course.is_deleted==False).all()
