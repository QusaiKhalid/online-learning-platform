from domain.interfaces.repositories.Iprogress_repository import IProgressRepository
from domain.models import Progress
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from typing import Optional

class ProgressRepository(BaseRepository[Progress], IProgressRepository):
    """Progress repository implementation using BaseRepository."""

    def __init__(self, db_session: Session):
        super().__init__(db_session, Progress)

    def get_progress(self, user_id: int, lesson_id: int) -> Optional[Progress]:
        """Fetch progress record by user ID and lesson ID."""
        return self.db_session.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.lesson_id == lesson_id
        ).first()  # Use .first() to get the first match or None if not found
