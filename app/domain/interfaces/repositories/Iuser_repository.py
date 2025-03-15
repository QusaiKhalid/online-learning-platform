from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models import User
from app.domain.interfaces.repositories.Ibase_repository import IBaseRepository

class IUserRepository(IBaseRepository[User], ABC):
    @abstractmethod
    def get_by_email(self, email: str, organization_id: int) -> Optional[User]:
        """Retrieve a user by email within a specific organization."""
        pass

    @abstractmethod
    def get_by_username(self, username: str, organization_id: int) -> Optional[User]:
        """Retrieve a user by username within a specific organization."""
        pass