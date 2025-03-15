from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Organization
from app.domain.interfaces.repositories.Ibase_repository import IBaseRepository

class IOrganizationRepository(IBaseRepository[Organization], ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Organization]:
        """Retrieve an organization by its unique name."""
        pass

    @abstractmethod
    def get_all_organizations(self) -> List[Organization]:
        """Retrieve all organizations."""
        pass