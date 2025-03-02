from typing import TypeVar, Generic, Optional, List
from app.domain.interfaces.repositories.Ibase_repository import IBaseRepository

T = TypeVar("T")  # Generic model type (User, Course, etc.)

class BaseService(Generic[T]):
    """Generic base service to handle common CRUD operations."""

    def __init__(self, repository: IBaseRepository[T]):
        self.repository = repository

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return self.repository.get_by_id(entity_id)

    def get_all(self) -> List[T]:
        return self.repository.get_all()

    def create(self, entity: T) -> T:
        return self.repository.create(entity)

    def update(self, entity_id: int, entity_data: dict) -> Optional[T]:
        return self.repository.update(entity_id, entity_data)

    def delete(self, entity_id: int) -> None:
        self.repository.delete(entity_id)
