from typing import Generic, TypeVar, List, Optional
from sqlalchemy.orm import Session
from app.domain.interfaces.repositories.Ibase_repository import IBaseRepository
from app.domain.models.organization import Organization
from sqlalchemy.exc import SQLAlchemyError
from app.domain.exceptions import EntityNotFoundError, DatabaseError

T = TypeVar("T")

class BaseRepository(IBaseRepository[T], Generic[T]):
    """Generic base repository implementation that adheres to IBaseRepository."""

    def __init__(self, db_session: Session, model: type):
        self.db_session = db_session
        self.model = model

    def get_by_id(self, entity_id: int, organization_id: str) -> Optional[T]:
        """
        Retrieve an entity by its ID within a specific organization.
        """
        try:
            # Validate organization_id
            organization = self.db_session.query(Organization).filter_by(
                keycloak_organization_id=organization_id, is_deleted=False
            ).first()
            if not organization:
                raise EntityNotFoundError(f"Organization with keycloak_organization_id {organization_id} not found.")
            # Query the entity with tenant isolation
            return self.db_session.query(self.model).filter_by(
                id=entity_id,
                keycloak_organization_id=organization.keycloak_organization_id,  # Use the organization's keycloak ID
                is_deleted=False
            ).first()

        except SQLAlchemyError as e:
            print(f"Database error occurred: {str(e)}")
            raise DatabaseError("An error occurred while accessing the database.") from e

    def get_all(self, organization_id: str) -> List[T]:
        """
        Retrieve all entities for a specific organization.
        Tenant isolation is enforced by requiring an organization_id.
        """
        try:
            # Validate organization_id
            organization = self.db_session.query(Organization).filter_by(
                keycloak_organization_id=organization_id, is_deleted=False
            ).first()
            if not organization:
                raise EntityNotFoundError(f"Organization with keycloak_organization_id {organization_id} not found.")

            # Query entities for the given organization
            return self.db_session.query(self.model).filter_by(
                is_deleted=False,
                keycloak_organization_id=organization.keycloak_organization_id,  # Use the organization's internal ID
            ).all()

        except SQLAlchemyError as e:
            print(f"Database error occurred: {str(e)}")
            raise DatabaseError("An error occurred while accessing the database.") from e

    def create(self, entity: T, keycloak_organization_id: str) -> T:
        """
        Create a new entity within a specific organization.
        Assumes the entity already has the keycloak_organization_id set.
        """
        try:
            # Validate organization by keycloak_organization_id
            organization = self.db_session.query(Organization).filter_by(
                keycloak_organization_id=keycloak_organization_id, is_deleted=False
            ).first()
            if not organization:
                raise EntityNotFoundError(f"Organization with keycloak_organization_id {keycloak_organization_id} not found.")

            # Ensure the entity's keycloak_organization_id matches the validated organization's ID
            if getattr(entity, "keycloak_organization_id") != organization.keycloak_organization_id:
                raise ValueError("Entity's keycloak_organization_id does not match the validated organization's ID.")

            # Add and commit the entity
            self.db_session.add(entity)
            self.db_session.commit()
            self.db_session.refresh(entity)
            return entity

        except SQLAlchemyError as e:
            print(f"Database error occurred: {str(e)}")
            raise DatabaseError("An error occurred while accessing the database.") from e

    def update(self, entity_id: int, entity_data: dict, organization_id: str) -> Optional[T]:
        """
        Update an existing entity within a specific organization.
        """
        try:
            # Validate organization_id
            organization = self.db_session.query(Organization).filter_by(
                keycloak_organization_id=organization_id, is_deleted=False
            ).first()
            if not organization:
                raise EntityNotFoundError(f"Organization with keycloak_organization_id {organization_id} not found.")

            # Fetch the entity with tenant isolation
            entity = self.db_session.query(self.model).filter_by(
                id=entity_id,
                keycloak_organization_id=organization.keycloak_organization_id,  # Use the organization's internal ID
                is_deleted=False
            ).first()

            if not entity:
                return None  # Entity not found

            # Update the entity with the provided data
            for key, value in entity_data.items():
                if hasattr(entity, key):  # Ensure the key exists in the entity
                    setattr(entity, key, value)

            self.db_session.commit()
            return entity

        except SQLAlchemyError as e:
            print(f"Database error occurred: {str(e)}")
            raise DatabaseError("An error occurred while accessing the database.") from e

    def delete(self, entity_id: int, organization_id: str) -> bool:
        """
        Soft delete an entity within a specific organization.
        """
        try:
            # Validate organization_id
            organization = self.db_session.query(Organization).filter_by(
                keycloak_organization_id=organization_id, is_deleted=False
            ).first()
            if not organization:
                raise EntityNotFoundError(f"Organization with keycloak_organization_id {organization_id} not found.")

            # Fetch the entity with tenant isolation
            entity = self.db_session.query(self.model).filter_by(
                id=entity_id,
                keycloak_organization_id=organization.keycloak_organization_id,  # Use the organization's internal ID
                is_deleted=False
            ).first()

            if not entity:
                return False  # Entity not found

            # Soft delete the entity
            entity.is_deleted = True
            self.db_session.commit()
            return True

        except SQLAlchemyError as e:
            print(f"Database error occurred: {str(e)}")
            raise DatabaseError("An error occurred while accessing the database.") from e