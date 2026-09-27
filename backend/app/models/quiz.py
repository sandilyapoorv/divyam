import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    time_limit_mins = Column(Integer, default=15)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    document = relationship("Document", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String, ForeignKey("quizzes.id"), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # List of 4 strings
    correct_index = Column(Integer, nullable=False)  # 0 to 3
    explanation = Column(Text, nullable=False)
    citation = Column(String, nullable=False)  # e.g., "PLFS Manual 2024, Page 14, Section 3.2"
    competency_id = Column(String, ForeignKey("competencies.id"), nullable=True)
    bloom_level = Column(String, default="Understanding")  # "Remembering", "Understanding", "Applying", "Analyzing"

    quiz = relationship("Quiz", back_populates="questions")
    competency = relationship("Competency")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(String, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=False)  # Percentage score e.g. 80.0
    total_questions = Column(Integer, nullable=False)
    correct_count = Column(Integer, nullable=False)
    answers = Column(JSON, nullable=False)  # dict: {question_id: selected_index}
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
