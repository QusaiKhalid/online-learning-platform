from typing import TypeVar, Generic, Optional, List
from sqlalchemy.orm import Session
from domain.interfaces.repositories.Ibase_repository import IBaseRepository

T = TypeVar("T")  # Generic model type (User, Course, etc.)

class BaseRepository(IBaseRepository[T], Generic[T]):
    """Generic base repository implementation for common CRUD operations."""

    def __init__(self, db_session: Session, model: type[T]):
        self.db_session = db_session
        self.model = model

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return self.db_session.query(self.model).filter(self.model.id == entity_id, self.model.is_deleted == False).first()

    def get_all(self) -> List[T]:
        return self.db_session.query(self.model).filter(self.model.is_deleted == False).all()

    def create(self, entity: T) -> T:
        self.db_session.add(entity)
        self.db_session.commit()
        self.db_session.refresh(entity)
        return entity

    def update(self, entity_id: int, entity_data: dict) -> Optional[T]:
        entity = self.get_by_id(entity_id)
        if not entity:
            return None
        for key, value in entity_data.items():
            setattr(entity, key, value)
        self.db_session.commit()
        return entity

    def delete(self, entity_id: int) -> bool:
        """Soft delete an entity by setting is_deleted=True instead of actual deletion."""
        entity = self.get_by_id(entity_id)
        if not entity:
            return False  # Entity not found
        entity.is_deleted = True
        self.db_session.commit()
        return True  # Deletion successful
