from datetime import datetime
from sqlalchemy import Column, BigInteger, ForeignKey, Boolean, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from ...extensions import db

class Enrollment(db.Model):
    __tablename__ = "enrollment"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete flag

    # Constraints
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="unique_enrollment"),)

    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")