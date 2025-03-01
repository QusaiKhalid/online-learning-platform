from typing import List
from app.domain.interfaces.repositories.Icourse_repository import ICourseRepository
from app.domain.models import Course
from app.application.services.base_servise import BaseService

class CourseService(BaseService[Course]):
    """Service for handling course-related operations."""

    def __init__(self, course_repository: ICourseRepository):
        super().__init__(course_repository)
        self.course_repository = course_repository

    def get_courses_by_instructor(self, instructor_id: int) -> List[Course]:
        """Fetch all courses assigned to a specific instructor."""
        return self.course_repository.get_by_instructor(instructor_id)