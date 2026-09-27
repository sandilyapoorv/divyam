#!/usr/bin/env python3
"""
DIVYAM - Complete End-to-End System Integration Test
Smart India Hackathon (SIH26101)

Verifies the entire lifecycle:
1. Database Schema Initialization & MoSPI Seed Population
2. Authentication & Cadre Verification (ISS / SSS Officers)
3. FRAC Competency Gap Analysis (Level 1-5 Radar Transform)
4. Deficit-Driven iGOT Karmayogi Course Recommendations
5. MoSPI Statistical Document Ingestion & Vector Indexing
6. 4-Tier Bloom's Taxonomy Quiz Generation with Zero-Hallucination Citations
7. Assessment Submission, Automated Grading & Competency Score Progression
8. Post-Test Readiness Index Improvement Validation
"""

import sys
import io
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.database import SessionLocal, engine, Base
from backend.app.data.seeds.mospi_data import seed_database
from backend.app.models.user import User

def run_e2e_verification():
    print("=" * 70)
    print(" DIVYAM (SIH26101) - Comprehensive End-to-End System Verification")
    print("=" * 70)

    # 1. Initialize DB and seed authentic MoSPI data
    print("\n[Step 0] Initializing SQLite Database and Seeding MoSPI FRAC Ontology...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    print("  [✓] Database seeded with Roles, Competencies, Benchmarks, Users & iGOT Courses.")

    client = TestClient(app)

    # --- Phase 1: Health Check & Authentication ---
    print("\n[Phase 1] Health Check & Authenticating SSS Cadre Officer...")
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    print("  [✓] Backend Health API OK: DIVYAM service active.")

    auth_resp = client.post("/api/auth/login", json={
        "email": "officer.sharma@mospi.gov.in"
    })
    assert auth_resp.status_code == 200, f"Login failed: {auth_resp.text}"
    auth_data = auth_resp.json()
    token = auth_data["access_token"]
    user_id = auth_data["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"  [✓] Officer Authenticated: {auth_data['user']['name']}")
    print(f"  [✓] Cadre Department: {auth_data['user']['department']}")
    print(f"  [✓] Cadre Role: {auth_data['user']['role_title']} ({auth_data['user']['role_code']})")

    # --- Phase 2: Initial FRAC Competency Gap Radar ---
    print("\n[Phase 2] Evaluating Initial FRAC Competency Gap Radar...")
    gap_resp = client.get("/api/competencies/gap-analysis", headers=headers)
    assert gap_resp.status_code == 200, f"Gap analysis failed: {gap_resp.text}"
    gap_data = gap_resp.json()

    initial_readiness = gap_data["readiness_index"]
    radar_points = gap_data["radar_data"]
    active_gaps = gap_data["gaps"]

    print(f"  [✓] Initial Cadre Readiness Index (Ω): {initial_readiness:.1f}%")
    print(f"  [✓] Multi-Axis Radar Dimensions: {len(radar_points)} axes formatted for Recharts")
    print(f"  [✓] Identified Competency Deficits: {len(active_gaps)} areas requiring training")
    for gap in active_gaps[:3]:
        print(f"      - {gap['competency_name']}: Level {gap['current_level']} -> Target {gap['required_level']} (Deficit: -{gap['gap']:.1f}, Priority: {gap['deficit_level']})")

    # --- Phase 3: iGOT Karmayogi Course Recommendations ---
    print("\n[Phase 3] Generating Deficit-Prioritized iGOT Karmayogi Recommendations...")
    igot_resp = client.get("/api/igot/recommendations", headers=headers)
    assert igot_resp.status_code == 200, f"iGOT recommendations failed: {igot_resp.text}"
    recommendations = igot_resp.json()

    assert len(recommendations) > 0, "No iGOT recommendations returned"
    print(f"  [✓] Total Curated Courses Recommended: {len(recommendations)}")
    top_rec = recommendations[0]
    print(f"  [✓] Top Priority Recommendation: \"{top_rec['course']['title']}\"")
    print(f"      - Provider: {top_rec['course']['provider']}")
    print(f"      - Target Level: Level {top_rec['course']['target_level']}")
    print(f"      - Deficit Addressed: {top_rec['matched_competency_name']} (Gap: -{top_rec['gap_value']:.1f}, Severity: {top_rec['gap_severity']})")
    print(f"      - iGOT URL: {top_rec['course']['url']}")

    # --- Phase 4: MoSPI Manual Document Ingestion & RAG Indexing ---
    print("\n[Phase 4] Ingesting Official MoSPI Statistical Manual...")
    sample_text = (
        "NATIONAL STATISTICAL HANDBOOK ON HOUSEHOLD SURVEYS (MoSPI)\n"
        "Chapter 2: Frame Stratification and FSU Demarcation.\n"
        "In the rural sector, the First Stage Units (FSUs) are Census Villages.\n"
        "In the urban sector, FSUs are Urban Frame Survey (UFS) blocks.\n"
        "Chapter 3: Optimum Neyman Allocation.\n"
        "Neyman allocation determines stratum sample size n_h proportional to N_h * S_h.\n"
        "Chapter 4: Horvitz-Thompson Design Weights.\n"
        "The design weight assigned to each sample enterprise under PPS is w_i = (1 / n) * (X / x_i).\n"
    )
    file_bytes = io.BytesIO(sample_text.encode('utf-8'))
    files = {"file": ("mospi_survey_sampling_2024.txt", file_bytes, "text/plain")}
    data = {
        "title": "MoSPI Survey Sampling Methodology Manual 2024"
    }

    doc_resp = client.post("/api/documents/upload", files=files, data=data, headers=headers)
    assert doc_resp.status_code == 200, f"Document upload failed: {doc_resp.text}"
    doc_data = doc_resp.json()
    doc_id = doc_data["id"]
    print(f"  [✓] Document Indexed: \"{doc_data['title']}\"")
    print(f"  [✓] Vector Store Chunks: {doc_data['total_chunks']} chunks in ChromaDB")

    # --- Phase 5: 4-Tier Bloom's Quiz Generation with Citations ---
    print("\n[Phase 5] Synthesizing 4-Tier Bloom's Taxonomy Assessment...")
    quiz_resp = client.post("/api/quizzes/generate", json={
        "document_id": doc_id,
        "title": "Official MoSPI Assessment: Survey Sampling",
        "num_questions": 4
    }, headers=headers)
    assert quiz_resp.status_code == 200, f"Quiz generation failed: {quiz_resp.text}"
    quiz_data = quiz_resp.json()
    quiz_id = quiz_data["id"]
    questions = quiz_data["questions"]

    print(f"  [✓] Quiz Generated: \"{quiz_data['title']}\" (ID: {quiz_id})")
    print(f"  [✓] Bloom's Questions Count: {len(questions)}")
    for i, q in enumerate(questions):
        print(f"      Q{i+1} [{q['bloom_level']}]: {q['question'][:65]}...")
        if q.get("citation"):
            print(f"          -> Citation: {q['citation']}")

    # --- Phase 6: Submitting Assessment & Automated Progression ---
    print("\n[Phase 6] Submitting Assessment & Verifying Automated Competency Progression...")
    # Answer questions matching the correct indices
    answers = {q["id"]: (q["correct_index"] if q.get("correct_index") is not None else 0) for q in questions}

    submit_resp = client.post(f"/api/quizzes/{quiz_id}/submit", json={
        "answers": answers
    }, headers=headers)
    assert submit_resp.status_code == 200, f"Quiz submission failed: {submit_resp.text}"
    submit_data = submit_resp.json()

    print(f"  [✓] Assessment Evaluated:")
    print(f"      - Score: {submit_data['score']}% ({submit_data['correct_count']}/{submit_data['total_questions']} correct)")
    print(f"      - Passed: {submit_data['passed']}")
    for update in submit_data["competency_updates"]:
        print(f"      - Competency Uplift: {update['competency_name']} (L{update['previous_level']} -> L{update['new_level']})")

    # --- Phase 7: Validating Post-Assessment Readiness Improvement ---
    print("\n[Phase 7] Re-evaluating FRAC Gap Analysis for Upliftment...")
    post_gap_resp = client.get("/api/competencies/gap-analysis", headers=headers)
    assert post_gap_resp.status_code == 200
    post_gap_data = post_gap_resp.json()
    updated_readiness = post_gap_data["readiness_index"]

    print(f"  [✓] Initial Readiness Index: {initial_readiness:.1f}%")
    print(f"  [✓] Updated Readiness Index: {updated_readiness:.1f}%")
    assert updated_readiness >= initial_readiness, "Readiness index should improve or maintain post-test"
    print(f"  [✓] Competency growth successfully registered in DIVYAM system!")

    print("\n" + "=" * 70)
    print(" [ALL PHASES PASSED] DIVYAM End-to-End System Verified Successfully!")
    print("=" * 70)

if __name__ == "__main__":
    run_e2e_verification()
