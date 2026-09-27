import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class CadreRole(Base):
    __tablename__ = "cadre_roles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    cadre = Column(String, nullable=False)  # "ISS", "SSS", "State DES"
    description = Column(Text, nullable=True)

    benchmarks = relationship("RoleBenchmark", back_populates="cadre_role", cascade="all, delete-orphan")
    users = relationship("User", back_populates="cadre_role")

class Competency(Base):
    __tablename__ = "competencies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "Domain", "Functional", "Behavioural"
    description = Column(Text, nullable=True)

    benchmarks = relationship("RoleBenchmark", back_populates="competency", cascade="all, delete-orphan")
    user_scores = relationship("UserCompetencyScore", back_populates="competency", cascade="all, delete-orphan")
    courses = relationship("IgotCourse", back_populates="competency")

class RoleBenchmark(Base):
    __tablename__ = "role_benchmarks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role_id = Column(String, ForeignKey("cadre_roles.id"), nullable=False)
    competency_id = Column(String, ForeignKey("competencies.id"), nullable=False)
    required_level = Column(Integer, nullable=False)  # 1 to 5
    criticality_weight = Column(Float, default=1.0)

    cadre_role = relationship("CadreRole", back_populates="benchmarks")
    competency = relationship("Competency", back_populates="benchmarks")
