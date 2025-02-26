# services/course_service.py
from domain.interfaces.repositories.Icourse_repository import ICourseRepository
from domain.models import Course
from typing import List, Optional

class CourseService:
    def __init__(self, course_repository: ICourseRepository):
        self.course_repository = course_repository

    def create_course(self, data: dict) -> Course:
        """Create a new course."""
        new_course = Course(**data)  # Assuming data is a dictionary that matches Course fields
        return self.course_repository.create(new_course)

    def get_course(self, course_id: int) -> Optional[Course]:
        """Get a course by ID."""
        return self.course_repository.get_by_id(course_id)

    def get_all_courses(self) -> List[Course]:
        """Get all courses."""
        return self.course_repository.get_all()

    def update_course(self, course_id: int, data: dict) -> Optional[Course]:
        """Update a course."""
        return self.course_repository.update(course_id, data)

    def delete_course(self, course_id: int) -> None:
        """Delete a course."""
        self.course_repository.delete(course_id)

    def get_courses_by_instructor(self, instructor_id: int) -> List[Course]:
        """Fetch all courses assigned to a specific instructor."""
        return self.course_repository.get_by_instructor(instructor_id)
