from typing import Optional
from app.domain.interfaces.repositories.Iprogress_repository import IProgressRepository
from app.domain.models import Progress
from app.application.services.base_servise import BaseService

class ProgressService(BaseService[Progress]):
    """Service for handling progress-related operations."""

    def __init__(self, progress_repository: IProgressRepository):
        super().__init__(progress_repository)
        self.progress_repository = progress_repository

    def get_progress_by_user_and_lesson(self, user_id: int, lesson_id: int) -> Optional[Progress]:
        """Fetch a progress record by user ID and lesson ID."""
        return self.progress_repository.get_progress(user_id, lesson_id)