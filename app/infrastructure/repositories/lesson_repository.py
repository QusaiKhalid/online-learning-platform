from domain.interfaces.repositories.Ilesson_repository import ILessonRepository
from domain.models import Lesson
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from typing import List

class LessonRepository(BaseRepository[Lesson], ILessonRepository):
    """Lesson repository implementation using BaseRepository."""

    def __init__(self, db_session: Session):
        super().__init__(db_session, Lesson)

    def get_by_course(self, course_id: int) -> List[Lesson]:
        """Fetch all lessons belonging to a specific course."""
        return self.db_session.query(Lesson).filter(Lesson.course_id == course_id).all()
