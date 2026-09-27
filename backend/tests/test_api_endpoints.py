import pytest
from fastapi.testclient import TestClient
from backend.app.core.database import SessionLocal, engine, Base
from backend.app.data.seeds.mospi_data import seed_database

def test_api_endpoints():
    from backend.app.main import app

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    client = TestClient(app)

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    assert res.json()["project"] == "DRIVYAM"

    # 2. Auth endpoints
    login_res = client.post("/api/auth/login", json={"email": "officer.sharma@mospi.gov.in"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    user_data = login_res.json()["user"]
    assert user_data["email"] == "officer.sharma@mospi.gov.in"

    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["name"] == "Sunil Sharma (SSS)"

    # 3. Competencies & Gap Analysis
    roles_res = client.get("/api/competencies/roles")
    assert roles_res.status_code == 200
    assert len(roles_res.json()) >= 3

    gap_res = client.get("/api/competencies/gap-analysis", headers={"Authorization": f"Bearer {token}"})
    assert gap_res.status_code == 200
    gap_data = gap_res.json()
    assert "readiness_index" in gap_data
    assert len(gap_data["gaps"]) > 0
    assert len(gap_data["radar_data"]) > 0

    # 4. iGOT Recommendations
    igot_res = client.get("/api/igot/recommendations", headers={"Authorization": f"Bearer {token}"})
    assert igot_res.status_code == 200
    recs = igot_res.json()
    assert len(recs) > 0
    assert recs[0]["course"]["url"].startswith("https://karmayogi.gov.in")

    catalog_res = client.get("/api/igot/catalog")
    assert catalog_res.status_code == 200
    assert len(catalog_res.json()) >= 5

    # 5. Documents List
    docs_res = client.get("/api/documents")
    assert docs_res.status_code == 200
    docs = docs_res.json()
    assert len(docs) >= 1

    # 6. Quizzes List & Quiz Details
    quizzes_res = client.get("/api/quizzes")
    assert quizzes_res.status_code == 200
    quizzes = quizzes_res.json()
    assert len(quizzes) >= 1
    quiz_id = quizzes[0]["id"]

    quiz_detail_res = client.get(f"/api/quizzes/{quiz_id}")
    assert quiz_detail_res.status_code == 200
    quiz_detail = quiz_detail_res.json()
    assert len(quiz_detail["questions"]) > 0
    # Client taking quiz should not receive answer keys
    for q in quiz_detail["questions"]:
        assert q["correct_index"] is None

    # 7. Submit Quiz
    questions = quiz_detail["questions"]
    answers = {q["id"]: 1 for q in questions}  # dummy answers
    submit_res = client.post(
        f"/api/quizzes/{quiz_id}/submit",
        json={"answers": answers},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert submit_res.status_code == 200
    result = submit_res.json()
    assert "score" in result
    assert "passed" in result
    assert len(result["review_questions"]) == len(questions)
    # Review questions must reveal correct index and explanations
    assert result["review_questions"][0]["correct_index"] is not None
    assert result["review_questions"][0]["citation"] is not None
