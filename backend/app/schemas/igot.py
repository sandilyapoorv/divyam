from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class IgotCourseSchema(BaseModel):
    id: str
    igot_id: str
    title: str
    provider: str
    description: Optional[str] = None
    duration_minutes: int
    competency_id: str
    competency_code: str
    competency_name: str
    competency_type: str
    target_level: int
    rating: float
    url: str
    thumbnail_url: Optional[str] = None

class IgotCourseRecommendation(BaseModel):
    course: IgotCourseSchema
    matched_competency_code: str
    matched_competency_name: str
    user_current_level: float
    target_required_level: float
    gap_value: float
    gap_severity: str  # "High", "Medium", "Low"
    priority_rank: int
    recommendation_reason: str
