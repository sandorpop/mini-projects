from .database import Base
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship

class Category(PyEnum):
    CARDIO = "cardio"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"
    
class MuscleGroup(PyEnum):
    CHEST = "chest"
    BACK = "back"
    LEGS = "legs"
    SHOULDERS = "shoulders"
    ARMS = "arms"
    CORE = "core"
    
class Status(PyEnum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    
class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    category = Column(Enum(Category), nullable=False)
    muscle_group = Column(Enum(MuscleGroup), nullable=False)
    is_seeded = Column(Boolean, nullable=False, server_default="false")
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    author = relationship("User")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    
    
class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    exercises = relationship("WorkoutExercise", lazy="joined", cascade="all, delete-orphan")
    
class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    workout_id = Column(Integer, ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    exercise = relationship("Exercise", lazy="joined")
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight_kg = Column(Float(precision=2), nullable=True)
    order = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    
class ScheduledWorkout(Base):
    __tablename__ = "scheduled_workouts"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    workout_id = Column(Integer, ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    workout = relationship("Workout", lazy="joined")
    user = relationship("User")
    workout_logs = relationship("WorkoutLog", cascade="all, delete-orphan", back_populates="scheduled_workout")
    scheduled_at = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.PENDING)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
class WorkoutLog(Base):
    __tablename__ = "workout_logs"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    scheduled_workout_id = Column(Integer, ForeignKey("scheduled_workouts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    scheduled_workout = relationship("ScheduledWorkout", back_populates="workout_logs")
    user = relationship("User")
    completed_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    duration_minutes = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    log_exercises = relationship("WorkoutLogExercise", lazy="joined", cascade="all, delete-orphan", back_populates="log")
    
class WorkoutLogExercise(Base):
    __tablename__ = "workout_log_exercises"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    log_id = Column(Integer, ForeignKey("workout_logs.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    log = relationship("WorkoutLog", lazy="joined", back_populates="log_exercises")
    exercise = relationship("Exercise", lazy="joined")
    sets_completed = Column(Integer, nullable=False)
    reps_completed = Column(Integer, nullable=False)
    weight_used_kg = Column(Float(precision=2), nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())