import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role_id = Column(String, ForeignKey("cadre_roles.id"), nullable=True)
    department = Column(String, default="MoSPI FOD")  # e.g., "FOD Kolkata", "NAD Delhi"
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    cadre_role = relationship("CadreRole", back_populates="users")
    competency_scores = relationship("UserCompetencyScore", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")

class UserCompetencyScore(Base):
    __tablename__ = "user_competency_scores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    competency_id = Column(String, ForeignKey("competencies.id"), nullable=False)
    current_level = Column(Float, nullable=False, default=1.0)  # 1.0 to 5.0
    last_assessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="competency_scores")
    competency = relationship("Competency", back_populates="user_scores")
