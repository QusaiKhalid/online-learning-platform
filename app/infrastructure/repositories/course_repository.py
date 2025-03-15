from domain.interfaces.repositories.Icourse_repository import ICourseRepository
from domain.models import Course, Organization
from app.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.domain.exceptions import EntityNotFoundError, DatabaseError

class CourseRepository(BaseRepository[Course], ICourseRepository):
    """Course repository implementation using BaseRepository."""

    def __init__(self, db_session: Session):
        super().__init__(db_session, Course)

    def get_by_instructor(self, instructor_id: int, organization_id: int) -> List[Course]:
        """
        Fetch all courses assigned to a specific instructor within a specific organization.
        Tenant isolation is enforced by requiring an organization_id.
        """
        try:
            # Validate organization_id
            organization = self.db_session.query(Organization).filter_by(
                keycloak_organization_id=organization_id, is_deleted=False
            ).first()
            if not organization:
                raise EntityNotFoundError(f"Organization with ID {organization_id} not found.")

            # Query courses created by the instructor within the specified organization
            return self.db_session.query(Course).filter(
                Course.created_by == instructor_id,
                Course.keycloak_organization_id == organization_id,
                Course.is_deleted == False
            ).all()

        except SQLAlchemyError as e:
            # Log the error and raise a custom DatabaseError
            print(f"Database error occurred: {str(e)}")
            raise DatabaseError("An error occurred while accessing the database.") from e