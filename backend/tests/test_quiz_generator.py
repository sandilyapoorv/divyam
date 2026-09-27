import pytest
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal, engine, Base
from backend.app.data.seeds.mospi_data import seed_database
from backend.app.models.user import User, UserCompetencyScore
from backend.app.models.quiz import Quiz, QuizQuestion

def test_quiz_generation_grading_and_competency_update():
    from backend.app.services.quiz_generator import QuizGeneratorService
    from backend.app.services.rag_engine import RagEngine

    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        seed_database(db)
        
        # Ingest a sample manual into RAG engine
        rag = RagEngine()
        doc_id = "doc-plfs-sample"
        rag.ingest_text(
            text_pages=[
                "Ministry of Statistics and Programme Implementation.\n"
                "The Periodic Labour Force Survey (PLFS) is designed to estimate key employment and unemployment "
                "indicators such as the Worker Population Ratio (WPR), Labour Force Participation Rate (LFPR), "
                "and Unemployment Rate (UR). In urban areas, an FSU is visited four times in a rotational panel.\n"
                "Under Usual Principal Status (UPS), activity status is determined based on the major time criterion "
                "(exceeding 182 days in the 365 days reference period)."
            ],
            doc_id=doc_id,
            title="PLFS Technical Guidelines 2024",
            filename="plfs_tech_guidelines.txt"
        )

        service = QuizGeneratorService(db=db, rag_engine=rag)

        # 1. Test Quiz Generation
        quiz = service.generate_quiz_from_document(
            doc_id=doc_id,
            title="AI Generated PLFS Knowledge Check",
            num_questions=3
        )
        assert quiz.id is not None
        assert len(quiz.questions) == 3

        # Verify Bloom's levels, citations, options
        for q in quiz.questions:
            assert len(q.options) == 4
            assert 0 <= q.correct_index <= 3
            assert q.bloom_level in ["Remembering", "Understanding", "Applying", "Analyzing"]
            assert q.citation is not None and "PLFS" in q.citation
            assert q.explanation is not None

        # 2. Test Quiz Grading & Competency Score Update
        user = db.query(User).filter(User.email == "officer.sharma@mospi.gov.in").first()
        assert user is not None

        # Find the competency score before attempt
        target_comp_id = quiz.questions[0].competency_id
        score_before = db.query(UserCompetencyScore).filter(
            UserCompetencyScore.user_id == user.id,
            UserCompetencyScore.competency_id == target_comp_id
        ).first()
        prev_level = score_before.current_level if score_before else 1.0

        # Submit answers (all correct)
        answers = {q.id: q.correct_index for q in quiz.questions}
        result = service.grade_quiz_attempt(
            user_id=user.id,
            quiz_id=quiz.id,
            answers=answers
        )

        assert result.score == 100.0
        assert result.correct_count == 3
        assert result.total_questions == 3
        assert result.passed is True
        assert len(result.competency_updates) > 0

        # Verify user score was upgraded
        db.refresh(score_before)
        assert score_before.current_level >= prev_level

    finally:
        db.close()
