from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from backend.app.core.database import get_db
from backend.app.api.auth import get_current_user
from backend.app.models.user import User, UserCompetencyScore
from backend.app.models.competency import CadreRole, Competency, RoleBenchmark
from backend.app.schemas.competency import (
    GapAnalysisResponse,
    BenchmarkItem,
    ScoreItem
)
from backend.app.services.frac_engine import (
    calculate_competency_gaps,
    calculate_readiness_index,
    format_radar_chart_data,
    evaluate_diagnostic_test
)

router = APIRouter(prefix="/competencies", tags=["Competencies & FRAC Engine"])

class CadreRoleSchema(BaseModel):
    id: str
    code: str
    title: str
    cadre: str
    description: str

class RoleSelectionRequest(BaseModel):
    role_id: str

class DiagnosticSubmissionRequest(BaseModel):
    answers: Dict[str, Dict[str, Any]]

@router.get("/roles", response_model=List[CadreRoleSchema])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(CadreRole).all()
    return [
        CadreRoleSchema(
            id=r.id,
            code=r.code,
            title=r.title,
            cadre=r.cadre,
            description=r.description or ""
        )
        for r in roles
    ]

@router.post("/select-role")
def select_role(
    payload: RoleSelectionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    role = db.query(CadreRole).filter(CadreRole.id == payload.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Cadre role not found")
    current_user.role_id = role.id
    db.commit()
    return {"message": f"Role updated to {role.title}", "role_id": role.id}

@router.get("/gap-analysis", response_model=GapAnalysisResponse)
def get_gap_analysis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    role_id = current_user.role_id
    if not role_id:
        role = db.query(CadreRole).first()
        if role:
            role_id = role.id
            current_user.role_id = role_id
            db.commit()

    role = db.query(CadreRole).filter(CadreRole.id == role_id).first()
    role_title = role.title if role else "Official Statistical Cadre"

    # Fetch benchmarks for role
    benchmarks_db = db.query(RoleBenchmark).filter(RoleBenchmark.role_id == role_id).all()
    benchmark_items = [
        BenchmarkItem(
            competency_code=b.competency.code,
            competency_name=b.competency.name,
            required_level=float(b.required_level),
            weight=b.criticality_weight
        )
        for b in benchmarks_db if b.competency
    ]

    # Fetch user scores
    scores_db = db.query(UserCompetencyScore).filter(UserCompetencyScore.user_id == current_user.id).all()
    score_map = {s.competency.code: s.current_level for s in scores_db if s.competency}

    # If user has no scores, initialize with 1.0 (baseline level)
    score_items = [
        ScoreItem(
            competency_code=b.competency_code,
            current_level=score_map.get(b.competency_code, 1.0)
        )
        for b in benchmark_items
    ]

    gaps = calculate_competency_gaps(benchmark_items, score_items)
    readiness = calculate_readiness_index(benchmark_items, score_items)
    radar_data = format_radar_chart_data(benchmark_items, score_items)

    return GapAnalysisResponse(
        role_title=role_title,
        readiness_index=readiness,
        gaps=gaps,
        radar_data=radar_data
    )

@router.post("/diagnostic")
def submit_diagnostic(
    payload: DiagnosticSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    diag_scores = evaluate_diagnostic_test(payload.answers)
    competencies = db.query(Competency).all()
    comp_lookup = {c.code: c.id for c in competencies}

    for comp_code, score_val in diag_scores.items():
        comp_id = comp_lookup.get(comp_code)
        if comp_id:
            user_score = db.query(UserCompetencyScore).filter(
                UserCompetencyScore.user_id == current_user.id,
                UserCompetencyScore.competency_id == comp_id
            ).first()
            if user_score:
                user_score.current_level = score_val
            else:
                user_score = UserCompetencyScore(
                    user_id=current_user.id,
                    competency_id=comp_id,
                    current_level=score_val
                )
                db.add(user_score)

    db.commit()
    return {"message": "Diagnostic baseline assessment successfully recorded", "scores": diag_scores}
