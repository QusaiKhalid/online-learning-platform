from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ...extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    keycloak_id = Column(String(36), unique=True, nullable=True)  # Keycloak user ID (UUID format)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum("student", "instructor", "admin", "teacher", name="user_role"), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete flag

    # Multi-tenancy: Add organization_id to associate users with organizations
    keycloak_organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)

    # Relationships
    courses_created = relationship("Course", back_populates="creator")
    enrollments = relationship("Enrollment", back_populates="user")
    progress = relationship("Progress", back_populates="user")
    organization = relationship("Organization", back_populates="users")