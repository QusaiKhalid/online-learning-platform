from typing import List
from app.domain.interfaces.repositories.Ilesson_repository import ILessonRepository
from app.domain.models import Lesson
from app.application.services.base_servise import BaseService

class LessonService(BaseService[Lesson]):
    """Service for handling lesson-related operations."""

    def __init__(self, lesson_repository: ILessonRepository):
        super().__init__(lesson_repository)
        self.lesson_repository = lesson_repository

    def get_lessons_by_course(self, course_id: int) -> List[Lesson]:
        """Fetch all lessons belonging to a specific course."""
        return self.lesson_repository.get_by_course(course_id)