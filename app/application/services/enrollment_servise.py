from typing import Optional
from app.domain.interfaces.repositories.Ienrollment_repository import IEnrollmentRepository
from app.domain.models import Enrollment
from app.application.services.base_servise import BaseService

class EnrollmentService(BaseService[Enrollment]):
    """Service for handling enrollment-related operations."""

    def __init__(self, enrollment_repository: IEnrollmentRepository):
        super().__init__(enrollment_repository)
        self.enrollment_repository = enrollment_repository

    def get_enrollment_by_user_and_course(self, user_id: int, course_id: int) -> Optional[Enrollment]:
        """Fetch an enrollment by user ID and course ID."""
        return self.enrollment_repository.get_by_user_and_course(user_id, course_id)