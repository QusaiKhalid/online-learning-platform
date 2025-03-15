from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship
from ...extensions import db

class Organization(db.Model):
    __tablename__ = "organizations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)  # Organization name
    keycloak_organization_id = Column(String(36), unique=True, nullable=False)  # Keycloak organization ID (UUID format)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete flag

    # Relationships
    users = relationship("User", back_populates="organization")
    courses = relationship("Course", back_populates="organization")