from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models import Progress
from app.domain.interfaces.repositories.Ibase_repository import BaseRepository

class IProgressRepository(BaseRepository[Progress], ABC):
    """Interface for tracking user progress on lessons."""

    @abstractmethod
    def get_progress(self, user_id: int, lesson_id: int) -> Optional[Progress]:
        pass
