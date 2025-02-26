from typing import List, Optional
from domain.models import Course
from domain.interfaces.repositories.Icourse_repository import ICourseRepository

class CourseService:
    """Service class for managing courses."""

    def __init__(self, course_repository: ICourseRepository):
        self.course_repository = course_repository

    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        """Get a course by its ID."""
        return self.course_repository.get_by_id(course_id)

    def get_all_courses(self) -> List[Course]:
        """Get all courses."""
        return self.course_repository.get_all()

    def create_course(self, title: str, description: str, created_by: int, status: str) -> Course:
        """Create a new course."""
        new_course = Course(title=title, description=description, created_by=created_by, status=status)
        return self.course_repository.create(new_course)

    def update_course(self, course_id: int, course_data: dict) -> Optional[Course]:
        """Update an existing course."""
        return self.course_repository.update(course_id, course_data)

    def delete_course(self, course_id: int) -> None:
        """Soft delete a course."""
        self.course_repository.delete(course_id)

    def get_courses_by_instructor(self, instructor_id: int) -> List[Course]:
        """Get courses by instructor ID."""
        return self.course_repository.get_by_instructor(instructor_id)
