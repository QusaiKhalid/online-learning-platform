class EntityNotFoundError(Exception):
    """Raised when an entity (e.g., organization) is not found."""
    pass

class DatabaseError(Exception):
    """Raised when a database-related error occurs."""
    pass