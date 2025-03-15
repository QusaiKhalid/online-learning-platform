from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")

class IBaseRepository(ABC, Generic[T]):
    """Base repository interface defining common CRUD operations for multi-tenancy."""

    @abstractmethod
    def get_by_id(self, entity_id: int, organization_id: int) -> Optional[T]:
        """
        Retrieve an entity by its ID within a specific organization.
        Tenant isolation is enforced by requiring an organization_id.
        """
        pass

    @abstractmethod
    def get_all(self, organization_id: int) -> List[T]:
        """
        Retrieve all entities for a specific organization.
        Tenant isolation is enforced by requiring an organization_id.
        """
        pass

    @abstractmethod
    def create(self, entity: T, organization_id: int) -> T:
        """
        Create a new entity within a specific organization.
        Tenant isolation is enforced by requiring an organization_id.
        """
        pass

    @abstractmethod
    def update(self, entity_id: int, entity_data: dict, organization_id: int) -> Optional[T]:
        """
        Update an existing entity within a specific organization.
        Tenant isolation is enforced by requiring an organization_id.
        """
        pass

    @abstractmethod
    def delete(self, entity_id: int, organization_id: int) -> bool:
        """
        Soft delete an entity within a specific organization.
        Tenant isolation is enforced by requiring an organization_id.
        Returns True if the deletion was successful, False otherwise.
        """
        pass