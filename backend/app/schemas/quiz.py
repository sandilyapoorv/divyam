from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class QuestionOption(BaseModel):
    index: int
    text: str

class QuizQuestionSchema(BaseModel):
    id: str
    quiz_id: str
    question: str
    options: List[str]
    correct_index: Optional[int] = None  # Hidden during test, visible during review
    explanation: Optional[str] = None
    citation: str
    competency_id: Optional[str] = None
    competency_code: Optional[str] = None
    competency_name: Optional[str] = None
    bloom_level: str

class QuizSchema(BaseModel):
    id: str
    title: str
    document_id: Optional[str] = None
    document_title: Optional[str] = None
    time_limit_mins: int
    total_questions: int
    created_at: datetime
    questions: Optional[List[QuizQuestionSchema]] = None

class QuizSubmissionRequest(BaseModel):
    answers: Dict[str, int]  # {question_id: selected_index}

class CompetencyScoreUpdate(BaseModel):
    competency_code: str
    competency_name: str
    previous_level: float
    new_level: float
    delta: float

class QuizAttemptResult(BaseModel):
    attempt_id: str
    quiz_id: str
    user_id: str
    score: float
    total_questions: int
    correct_count: int
    passed: bool
    review_questions: List[QuizQuestionSchema]
    competency_updates: List[CompetencyScoreUpdate]
    completed_at: datetime
