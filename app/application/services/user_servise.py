from app.domain.interfaces.repositories.Iuser_repository import IUserRepository
from app.domain.models import User
from typing import Optional, List

class UserService:
    """Service for handling user-related operations."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Fetch a user by ID."""
        return self.user_repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by email."""
        return self.user_repository.get_by_email(email)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Fetch a user by username."""
        return self.user_repository.get_by_username(username)

    def get_all_users(self) -> List[User]:
        """Fetch all users."""
        return self.user_repository.get_all()

    def create_user(self, user_data: dict) -> User:
        """Create a new user."""
        new_user = User(**user_data)
        return self.user_repository.create(new_user)

    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        """Update an existing user."""
        return self.user_repository.update(user_id, user_data)

    def delete_user(self, user_id: int) -> bool:
        """Soft delete a user by setting `is_deleted=True` instead of actual deletion."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False
        return bool(self.user_repository.update(user_id, {"is_deleted": True}))
