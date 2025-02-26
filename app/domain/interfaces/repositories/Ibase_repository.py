from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")

class IBaseRepository(ABC, Generic[T]):
    """Base repository interface defining common CRUD operations."""

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity_id: int, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        pass
