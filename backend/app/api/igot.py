from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.core.database import get_db
from backend.app.api.auth import get_current_user
from backend.app.api.competencies import get_gap_analysis
from backend.app.models.user import User
from backend.app.schemas.igot import IgotCourseSchema, IgotCourseRecommendation
from backend.app.services.igot_client import IgotClient

router = APIRouter(prefix="/igot", tags=["iGOT Karmayogi Integration"])

@router.get("/recommendations", response_model=List[IgotCourseRecommendation])
def get_recommendations(
    limit: int = Query(default=5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    gap_analysis = get_gap_analysis(current_user=current_user, db=db)
    client = IgotClient(db=db)
    recommendations = client.recommend_courses(user_gaps=gap_analysis.gaps, limit=limit)
    return recommendations

@router.get("/catalog", response_model=List[IgotCourseSchema])
def get_catalog(
    competency_type: Optional[str] = Query(default=None, description="Filter by Domain, Functional, or Behavioural"),
    db: Session = Depends(get_db)
):
    client = IgotClient(db=db)
    return client.get_catalog(competency_type=competency_type)
