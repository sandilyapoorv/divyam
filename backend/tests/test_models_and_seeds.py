import pytest
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal, engine, Base

def test_models_and_seeds():
    from backend.app.models.competency import CadreRole, Competency, RoleBenchmark
    from backend.app.models.user import User, UserCompetencyScore
    from backend.app.models.document import Document
    from backend.app.models.quiz import Quiz, QuizQuestion, QuizAttempt
    from backend.app.models.igot import IgotCourse
    from backend.app.data.seeds.mospi_data import seed_database

    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # Seed database
        seed_database(db)
        
        # Verify roles seeded
        roles = db.query(CadreRole).all()
        assert len(roles) >= 3
        role_codes = [r.code for r in roles]
        assert "ROLE_STAT_INV_2" in role_codes
        
        # Verify competencies seeded (Domain, Functional, Behavioural)
        comps = db.query(Competency).all()
        assert len(comps) >= 6
        comp_types = set(c.type for c in comps)
        assert {"Domain", "Functional", "Behavioural"}.issubset(comp_types)
        
        # Verify benchmarks seeded
        benchmarks = db.query(RoleBenchmark).all()
        assert len(benchmarks) > 0
        
        # Verify default test user exists
        user = db.query(User).filter(User.email == "officer.sharma@mospi.gov.in").first()
        assert user is not None
        assert user.cadre_role is not None
        
        # Verify user has scores
        scores = db.query(UserCompetencyScore).filter(UserCompetencyScore.user_id == user.id).all()
        assert len(scores) > 0
        
        # Verify iGOT courses seeded
        courses = db.query(IgotCourse).all()
        assert len(courses) >= 4
        
    finally:
        db.close()
