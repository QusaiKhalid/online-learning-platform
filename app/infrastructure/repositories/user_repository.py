from app.domain.interfaces.repositories.Iuser_repository import IUserRepository
from app.domain.models import User
from app.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from app.domain.exceptions import DatabaseError

class UserRepository(BaseRepository[User], IUserRepository):
    """User repository implementation using BaseRepository."""

    def __init__(self, db_session: Session):
        super().__init__(db_session, User)

    def get_by_email(self, email: str, organization_id: int) -> Optional[User]:
        """
        Fetch a user by email within a specific organization.
        Tenant isolation is enforced by requiring an organization_id.
        """
        try:
            # Query the user with tenant isolation
            return self.db_session.query(User).filter(
                User.email == email,
                User.Keycloak_organization_id == organization_id,
                User.is_deleted == False
            ).first()

        except SQLAlchemyError as e:
            # Log the error and raise a custom DatabaseError
            print(f"Database error occurred: {str(e)}")
            raise DatabaseError("An error occurred while accessing the database.") from e

    def get_by_username(self, username: str, organization_id: int) -> Optional[User]:
        """
        Fetch a user by username within a specific organization.
        Tenant isolation is enforced by requiring an organization_id.
        """
        try:
            # Query the user with tenant isolation
            return self.db_session.query(User).filter(
                User.username == username,
                User.Keycloak_organization_id == organization_id,
                User.is_deleted == False
            ).first()

        except SQLAlchemyError as e:
            # Log the error and raise a custom DatabaseError
            print(f"Database error occurred: {str(e)}")
            raise DatabaseError("An error occurred while accessing the database.") from e