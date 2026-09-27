import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class IgotCourse(Base):
    __tablename__ = "igot_courses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    igot_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    provider = Column(String, default="NSSTA / MoSPI")  # NSSTA, Karmayogi Bharat, ISI Kolkata
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, default=120)
    competency_id = Column(String, ForeignKey("competencies.id"), nullable=False)
    target_level = Column(Integer, default=3)  # 1 to 5
    rating = Column(Float, default=4.8)
    url = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)

    competency = relationship("Competency", back_populates="courses")
