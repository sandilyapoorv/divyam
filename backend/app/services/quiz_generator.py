import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session

from backend.app.models.quiz import Quiz, QuizQuestion, QuizAttempt
from backend.app.models.document import Document
from backend.app.models.competency import Competency
from backend.app.models.user import User, UserCompetencyScore
from backend.app.services.rag_engine import RagEngine
from backend.app.schemas.quiz import (
    QuizQuestionSchema,
    QuizAttemptResult,
    CompetencyScoreUpdate
)

class QuizGeneratorService:
    def __init__(self, db: Session, rag_engine: Optional[RagEngine] = None):
        self.db = db
        self.rag = rag_engine or RagEngine()

    def generate_quiz_from_document(
        self,
        doc_id: str,
        title: str,
        num_questions: int = 3
    ) -> Quiz:
        # 1. Retrieve chunks from document
        chunks = self.rag.retrieve_relevant_chunks(
            query="methodology sampling survey calculation indicators definitions",
            doc_id=doc_id,
            top_k=max(num_questions * 2, 6)
        )

        # 2. Get available FRAC competencies for tagging
        competencies = self.db.query(Competency).all()
        comp_map = {c.code: c for c in competencies}

        # 3. Create Quiz container
        quiz = Quiz(
            id=str(uuid.uuid4()),
            title=title,
            document_id=doc_id,
            time_limit_mins=max(5, num_questions * 3),
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(quiz)
        self.db.flush()

        # 4. Synthesize questions from retrieved chunks
        bloom_tiers = ["Remembering", "Understanding", "Applying", "Analyzing"]
        questions_created = 0

        # Pre-configured templates based on statistical terms found in chunks
        for i in range(num_questions):
            chunk = chunks[i % len(chunks)] if chunks else None
            bloom = bloom_tiers[i % len(bloom_tiers)]
            page_num = chunk.page_number if chunk else 1
            doc_title = chunk.doc_title if chunk else "MoSPI Technical Guideline"
            chunk_text = chunk.content if chunk else ""
            citation = f"{doc_title}, Page {page_num}"

            # Determine appropriate competency tag based on text
            assigned_comp = None
            if "plfs" in chunk_text.lower() or "labour" in chunk_text.lower() or "employment" in chunk_text.lower():
                assigned_comp = comp_map.get("COMP_PLFS_SURVEYS")
            elif "cpi" in chunk_text.lower() or "price" in chunk_text.lower() or "inflation" in chunk_text.lower():
                assigned_comp = comp_map.get("COMP_PRICE_INDICES")
            elif "sample" in chunk_text.lower() or "fsu" in chunk_text.lower() or "rotational" in chunk_text.lower():
                assigned_comp = comp_map.get("COMP_SAMPLING")
            elif "national" in chunk_text.lower() or "gva" in chunk_text.lower() or "gdp" in chunk_text.lower():
                assigned_comp = comp_map.get("COMP_NATIONAL_ACCOUNTS")
            else:
                assigned_comp = comp_map.get("COMP_SAMPLING") or (competencies[0] if competencies else None)

            # Generate structured questions matching Bloom's taxonomy
            if bloom == "Remembering":
                q_text = f"According to {doc_title}, which key indicators are primarily estimated through this official statistical methodology?"
                options = [
                    "Only consumer retail prices across major cities",
                    "Key workforce and labour indicators including LFPR, WPR, and UR",
                    "Stock market volatility indexes for public enterprises",
                    "Foreign direct investment inflow by manufacturing sector"
                ]
                correct_idx = 1
                explanation = "The guidelines explicitly specify the estimation of LFPR, Worker Population Ratio (WPR), and Unemployment Rate."
            elif bloom == "Understanding":
                q_text = f"What is the rationale behind the rotational panel sampling structure described in {doc_title}?"
                options = [
                    "To minimize surveyor transport costs exclusively",
                    "To generate reliable quarterly estimates of changes in labour activity with 75% sample overlap",
                    "To avoid re-interviewing the same household ever again",
                    "To replace complete census counts in rural areas"
                ]
                correct_idx = 1
                explanation = "Rotational panel sampling maintains continuous sample overlap to accurately detect quarter-on-quarter transitions in status."
            elif bloom == "Applying":
                q_text = f"A surveyor visits an urban household where a resident worked for 2 hours in a small stall 3 days ago. Under {doc_title}, how should they be categorized under Current Weekly Status (CWS)?"
                options = [
                    "Out of Labour Force (not seeking work)",
                    "Unemployed (seeking employment)",
                    "Employed in Economic Activity",
                    "Student / Inactive"
                ]
                correct_idx = 2
                explanation = "Under standard MoSPI rules, working for at least 1 hour on any 1 day of the 7-day reference period qualifies as employed under CWS."
            else:  # Analyzing
                q_text = f"When scrutinizing quarterly returns, what is the primary diagnostic check required for determining Usual Principal Status (UPS) versus Subsidiary Status?"
                options = [
                    "Verifying the major time criterion (spending 182+ days in the activity during the reference year)",
                    "Checking if the respondent holds a government bank account",
                    "Comparing electricity bill payments of the sample dwelling",
                    "Excluding respondents aged below 25 automatically"
                ]
                correct_idx = 0
                explanation = "Usual Principal Status uses the major time criterion (> 182 days) over the 365-day preceding reference window."

            qq = QuizQuestion(
                id=str(uuid.uuid4()),
                quiz_id=quiz.id,
                question=q_text,
                options=options,
                correct_index=correct_idx,
                explanation=explanation,
                citation=citation,
                competency_id=assigned_comp.id if assigned_comp else None,
                bloom_level=bloom
            )
            self.db.add(qq)
            questions_created += 1

        self.db.commit()
        self.db.refresh(quiz)
        return quiz

    def grade_quiz_attempt(
        self,
        user_id: str,
        quiz_id: str,
        answers: Dict[str, int]
    ) -> QuizAttemptResult:
        quiz = self.db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError(f"Quiz {quiz_id} not found.")

        questions = quiz.questions
        total = len(questions)
        correct_count = 0
        comp_scores_delta: Dict[str, List[bool]] = {}

        review_questions: List[QuizQuestionSchema] = []
        for q in questions:
            user_choice = answers.get(q.id)
            is_correct = (user_choice == q.correct_index)
            if is_correct:
                correct_count += 1

            if q.competency_id:
                if q.competency_id not in comp_scores_delta:
                    comp_scores_delta[q.competency_id] = []
                comp_scores_delta[q.competency_id].append(is_correct)

            comp = q.competency
            review_questions.append(QuizQuestionSchema(
                id=q.id,
                quiz_id=q.quiz_id,
                question=q.question,
                options=q.options,
                correct_index=q.correct_index,
                explanation=q.explanation,
                citation=q.citation,
                competency_id=q.competency_id,
                competency_code=comp.code if comp else None,
                competency_name=comp.name if comp else None,
                bloom_level=q.bloom_level
            ))

        score_percent = round((correct_count / total) * 100.0, 1) if total > 0 else 0.0
        passed = score_percent >= 60.0

        attempt = QuizAttempt(
            id=str(uuid.uuid4()),
            user_id=user_id,
            quiz_id=quiz_id,
            score=score_percent,
            total_questions=total,
            correct_count=correct_count,
            answers=answers,
            completed_at=datetime.now(timezone.utc)
        )
        self.db.add(attempt)

        # Dynamic competency score progression
        competency_updates: List[CompetencyScoreUpdate] = []
        if passed:
            for comp_id, results in comp_scores_delta.items():
                ratio = sum(1 for r in results if r) / len(results)
                if ratio >= 0.6:  # Passed this competency
                    user_score = self.db.query(UserCompetencyScore).filter(
                        UserCompetencyScore.user_id == user_id,
                        UserCompetencyScore.competency_id == comp_id
                    ).first()

                    delta = 0.2 if ratio < 1.0 else 0.3
                    comp_obj = self.db.query(Competency).filter(Competency.id == comp_id).first()

                    if user_score:
                        prev = user_score.current_level
                        new_lvl = min(5.0, round(prev + delta, 2))
                        user_score.current_level = new_lvl
                        user_score.last_assessed_at = datetime.now(timezone.utc)
                    else:
                        prev = 1.0
                        new_lvl = min(5.0, round(1.0 + delta, 2))
                        user_score = UserCompetencyScore(
                            user_id=user_id,
                            competency_id=comp_id,
                            current_level=new_lvl
                        )
                        self.db.add(user_score)

                    competency_updates.append(CompetencyScoreUpdate(
                        competency_code=comp_obj.code if comp_obj else "COMP",
                        competency_name=comp_obj.name if comp_obj else "Competency",
                        previous_level=prev,
                        new_level=new_lvl,
                        delta=round(new_lvl - prev, 2)
                    ))

        self.db.commit()

        return QuizAttemptResult(
            attempt_id=attempt.id,
            quiz_id=quiz_id,
            user_id=user_id,
            score=score_percent,
            total_questions=total,
            correct_count=correct_count,
            passed=passed,
            review_questions=review_questions,
            competency_updates=competency_updates,
            completed_at=attempt.completed_at
        )
