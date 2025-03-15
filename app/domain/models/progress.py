from sqlalchemy import Column, BigInteger, ForeignKey, Boolean, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from ...extensions import db

class Progress(db.Model):
    __tablename__ = "progress"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(BigInteger, ForeignKey("lessons.id"), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    watched_duration = Column(BigInteger, default=0, nullable=False)
    completed_at = Column(TIMESTAMP)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete flag

    # Constraints
    __table_args__ = (UniqueConstraint("user_id", "lesson_id", name="unique_progress"),)

    # Relationships
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")