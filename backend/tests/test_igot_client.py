import pytest
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal, engine, Base
from backend.app.data.seeds.mospi_data import seed_database
from backend.app.schemas.competency import CompetencyGap

def test_igot_recommendations_and_catalog():
    from backend.app.services.igot_client import IgotClient

    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        seed_database(db)
        client = IgotClient(db=db)

        # 1. Test Course Catalog retrieval
        catalog = client.get_catalog()
        assert len(catalog) >= 5
        
        # Test filter by competency type
        domain_courses = client.get_catalog(competency_type="Domain")
        assert len(domain_courses) > 0
        for c in domain_courses:
            assert c.competency_type == "Domain"

        # 2. Test Recommendation for Officer with specific deficits
        # User has a severe gap in COMP_PLFS_SURVEYS (gap: 1.5) and COMP_PRICE_INDICES (gap: 1.2)
        mock_gaps = [
            CompetencyGap(
                competency_code="COMP_PLFS_SURVEYS",
                competency_name="Periodic Labour Force Survey",
                required_level=4.0,
                current_level=2.5,
                gap=1.5,
                deficit_level="High",
                criticality_weight=1.5
            ),
            CompetencyGap(
                competency_code="COMP_PRICE_INDICES",
                competency_name="Price & Inflation Indices",
                required_level=3.0,
                current_level=1.8,
                gap=1.2,
                deficit_level="Medium",
                criticality_weight=1.2
            ),
            CompetencyGap(
                competency_code="COMP_DATA_ETHICS",
                competency_name="Data Ethics",
                required_level=4.0,
                current_level=4.0,
                gap=0.0,
                deficit_level="None",
                criticality_weight=1.0
            )
        ]

        recommendations = client.recommend_courses(user_gaps=mock_gaps, limit=4)
        assert len(recommendations) > 0

        # Top recommendation should match the highest deficit competency
        top_rec = recommendations[0]
        assert top_rec.matched_competency_code in ["COMP_PLFS_SURVEYS", "COMP_PRICE_INDICES"]
        assert top_rec.course.url.startswith("https://karmayogi.gov.in")
        assert top_rec.gap_severity in ["High", "Medium"]
        assert top_rec.priority_rank == 1

        # Zero deficit should not dominate recommendations
        matched_codes = [r.matched_competency_code for r in recommendations]
        assert "COMP_PLFS_SURVEYS" in matched_codes
    finally:
        db.close()
