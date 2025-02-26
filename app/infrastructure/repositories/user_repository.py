from app.domain.interfaces.repositories.Iuser_repository import IUserRepository
from app.domain.models import User
from app.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from typing import Optional

class UserRepository(BaseRepository[User], IUserRepository):
    """User repository implementation using BaseRepository."""

    def __init__(self, db_session: Session):
        super().__init__(db_session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by email."""
        return self.db_session.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Fetch a user by username."""
        return self.db_session.query(User).filter(User.username == username).first()
