from typing import Optional
from app.domain.interfaces.repositories.Iuser_repository import IUserRepository
from app.domain.models import User
from app.application.services.base_servise import BaseService

class UserService(BaseService[User]):
    """Service for handling user-related operations."""

    def __init__(self, user_repository: IUserRepository):
        super().__init__(user_repository)
        self.user_repository = user_repository

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by their email."""
        return self.user_repository.get_by_email(email)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Fetch a user by their username."""
        return self.user_repository.get_by_username(username)