from sqlalchemy import Column, BigInteger, String, Text, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ...extensions import db

class Course(db.Model):
    __tablename__ = "courses"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    status = Column(Enum("draft", "published", name="course_status"), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete flag

    # Multi-tenancy: Add organization_id to associate courses with organizations
    keycloak_organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)

    # Relationships
    creator = relationship("User", back_populates="courses_created")
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    organization = relationship("Organization", back_populates="courses")