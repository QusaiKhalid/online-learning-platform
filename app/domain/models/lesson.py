from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ...extensions import db

class Lesson(db.Model):
    __tablename__ = "lessons"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    course_id = Column(BigInteger, ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    video_url = Column(String(255), nullable=False)
    thumbnail_url = Column(String(255))
    duration = Column(BigInteger)
    order = Column(BigInteger, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete flag

    # Relationships
    course = relationship("Course", back_populates="lessons")
    progress = relationship("Progress", back_populates="lesson")