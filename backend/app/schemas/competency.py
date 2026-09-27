from pydantic import BaseModel, Field
from typing import List, Optional

class BenchmarkItem(BaseModel):
    competency_code: str
    competency_name: str
    required_level: float = Field(ge=1.0, le=5.0)
    weight: float = 1.0

class ScoreItem(BaseModel):
    competency_code: str
    current_level: float = Field(ge=1.0, le=5.0)

class CompetencyGap(BaseModel):
    competency_code: str
    competency_name: str
    required_level: float
    current_level: float
    gap: float
    deficit_level: str  # "None", "Low", "Medium", "High"
    criticality_weight: float

class RadarAxisItem(BaseModel):
    competency: str
    competency_code: str
    required: float
    current: float
    gap: float

class GapAnalysisResponse(BaseModel):
    role_title: str
    readiness_index: float
    gaps: List[CompetencyGap]
    radar_data: List[RadarAxisItem]
