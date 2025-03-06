from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Enum,
    ForeignKey,
    Boolean,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from ..extensions import db
from sqlalchemy import Column, BigInteger, String, Boolean, Enum
from sqlalchemy.orm import relationship

# Define the Users table
class User(db.Model):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)  # Internal database ID
    keycloak_id = Column(String(36), unique=True, nullable=True)  # Keycloak user ID (UUID format)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum("student", "instructor", "admin", "teacher", name="user_role"), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete flag

    # Relationships
    courses_created = relationship("Course", back_populates="creator")
    enrollments = relationship("Enrollment", back_populates="user")
    progress = relationship("Progress", back_populates="user")


# Define the Courses table
class Course(db.Model):
    __tablename__ = "courses"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    status = Column(Enum("draft", "published", name="course_status"), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete flag

    # Relationships
    creator = relationship("User", back_populates="courses_created")
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")


# Define the Lessons table
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


# Define the Enrollment table (many-to-many relationship between Users and Courses)
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


# Define the Progress table (tracks student progress in lessons)
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
