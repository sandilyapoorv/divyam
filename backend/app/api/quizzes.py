from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from backend.app.core.database import get_db
from backend.app.api.auth import get_current_user
from backend.app.models.user import User
from backend.app.models.quiz import Quiz, QuizQuestion, QuizAttempt
from backend.app.schemas.quiz import (
    QuizSchema,
    QuizQuestionSchema,
    QuizSubmissionRequest,
    QuizAttemptResult
)
from backend.app.services.quiz_generator import QuizGeneratorService

router = APIRouter(prefix="/quizzes", tags=["Bloom's Taxonomy Assessments"])

class GenerateQuizRequest(BaseModel):
    document_id: str
    title: Optional[str] = None
    num_questions: int = 5

@router.post("/generate", response_model=QuizSchema)
def generate_quiz(
    payload: GenerateQuizRequest,
    db: Session = Depends(get_db)
):
    service = QuizGeneratorService(db=db)
    title = payload.title or "AI-Generated Assessment"
    quiz = service.generate_quiz_from_document(
        doc_id=payload.document_id,
        title=title,
        num_questions=payload.num_questions
    )
    
    return QuizSchema(
        id=quiz.id,
        title=quiz.title,
        document_id=quiz.document_id,
        document_title=quiz.document.title if quiz.document else "Official Document",
        time_limit_mins=quiz.time_limit_mins,
        total_questions=len(quiz.questions),
        created_at=quiz.created_at,
        questions=[
            QuizQuestionSchema(
                id=q.id,
                quiz_id=q.quiz_id,
                question=q.question,
                options=q.options,
                correct_index=q.correct_index,
                explanation=q.explanation,
                citation=q.citation,
                competency_id=q.competency_id,
                competency_code=q.competency.code if q.competency else None,
                competency_name=q.competency.name if q.competency else None,
                bloom_level=q.bloom_level
            )
            for q in quiz.questions
        ]
    )

@router.get("", response_model=List[QuizSchema])
def list_quizzes(db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).order_by(Quiz.created_at.desc()).all()
    return [
        QuizSchema(
            id=q.id,
            title=q.title,
            document_id=q.document_id,
            document_title=q.document.title if q.document else "MoSPI Technical Guideline",
            time_limit_mins=q.time_limit_mins,
            total_questions=len(q.questions),
            created_at=q.created_at
        )
        for q in quizzes
    ]

@router.get("/{quiz_id}", response_model=QuizSchema)
def get_quiz_detail(
    quiz_id: str,
    include_answers: bool = Query(default=False),
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions_schema = []
    for q in quiz.questions:
        questions_schema.append(QuizQuestionSchema(
            id=q.id,
            quiz_id=q.quiz_id,
            question=q.question,
            options=q.options,
            correct_index=q.correct_index if include_answers else None,
            explanation=q.explanation if include_answers else None,
            citation=q.citation,
            competency_id=q.competency_id,
            competency_code=q.competency.code if q.competency else None,
            competency_name=q.competency.name if q.competency else None,
            bloom_level=q.bloom_level
        ))

    return QuizSchema(
        id=quiz.id,
        title=quiz.title,
        document_id=quiz.document_id,
        document_title=quiz.document.title if quiz.document else "Official Document",
        time_limit_mins=quiz.time_limit_mins,
        total_questions=len(quiz.questions),
        created_at=quiz.created_at,
        questions=questions_schema
    )

@router.post("/{quiz_id}/submit", response_model=QuizAttemptResult)
def submit_quiz(
    quiz_id: str,
    payload: QuizSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = QuizGeneratorService(db=db)
    result = service.grade_quiz_attempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        answers=payload.answers
    )
    return result
