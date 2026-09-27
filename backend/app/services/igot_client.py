from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.models.igot import IgotCourse
from backend.app.models.competency import Competency
from backend.app.schemas.igot import IgotCourseSchema, IgotCourseRecommendation
from backend.app.schemas.competency import CompetencyGap

class IgotClient:
    """
    Adapter for iGOT Karmayogi ecosystem.
    Supports official GoI FRAC metadata schemas, sandbox catalog, and live endpoints.
    """
    def __init__(self, db: Session):
        self.db = db

    def _to_schema(self, course: IgotCourse) -> IgotCourseSchema:
        comp = course.competency
        return IgotCourseSchema(
            id=course.id,
            igot_id=course.igot_id,
            title=course.title,
            provider=course.provider,
            description=course.description,
            duration_minutes=course.duration_minutes,
            competency_id=course.competency_id,
            competency_code=comp.code if comp else "UNKNOWN",
            competency_name=comp.name if comp else "Unknown Competency",
            competency_type=comp.type if comp else "Domain",
            target_level=course.target_level,
            rating=course.rating,
            url=course.url,
            thumbnail_url=course.thumbnail_url
        )

    def get_catalog(self, competency_type: Optional[str] = None) -> List[IgotCourseSchema]:
        query = self.db.query(IgotCourse).join(Competency)
        if competency_type:
            query = query.filter(Competency.type == competency_type)
        courses = query.order_by(IgotCourse.rating.desc()).all()
        return [self._to_schema(c) for c in courses]

    def recommend_courses(
        self,
        user_gaps: List[CompetencyGap],
        limit: int = 5
    ) -> List[IgotCourseRecommendation]:
        """
        Ranks and pairs iGOT Karmayogi courses with officer's identified competency deficits.
        Prioritizes by gap severity * criticality weight, then course rating.
        """
        # Build gap dictionary for quick lookup
        gap_lookup = {g.competency_code: g for g in user_gaps if g.gap > 0}
        
        # Fetch all courses from db
        all_courses = self.db.query(IgotCourse).join(Competency).all()
        
        scored_recommendations = []
        for course in all_courses:
            comp_code = course.competency.code if course.competency else None
            gap_item = gap_lookup.get(comp_code)
            
            if gap_item:
                priority_score = gap_item.gap * gap_item.criticality_weight * 10.0 + course.rating
                reason = (
                    f"Recommended to bridge your {gap_item.deficit_level.lower()} deficit of {gap_item.gap:.1f} "
                    f"in '{gap_item.competency_name}' (Target Level {gap_item.required_level:.0f})."
                )
                scored_recommendations.append((
                    priority_score,
                    IgotCourseRecommendation(
                        course=self._to_schema(course),
                        matched_competency_code=gap_item.competency_code,
                        matched_competency_name=gap_item.competency_name,
                        user_current_level=gap_item.current_level,
                        target_required_level=gap_item.required_level,
                        gap_value=gap_item.gap,
                        gap_severity=gap_item.deficit_level,
                        priority_rank=0,  # Will assign after sort
                        recommendation_reason=reason
                    )
                ))

        # Sort by priority score descending
        scored_recommendations.sort(key=lambda x: x[0], reverse=True)
        final_recs = [item[1] for item in scored_recommendations[:limit]]

        # If user has few or no deficits, backfill with top foundational courses
        if len(final_recs) < limit:
            existing_ids = {r.course.id for r in final_recs}
            for course in all_courses:
                if course.id not in existing_ids:
                    final_recs.append(IgotCourseRecommendation(
                        course=self._to_schema(course),
                        matched_competency_code=course.competency.code if course.competency else "GEN_STAT",
                        matched_competency_name=course.competency.name if course.competency else "Official Statistics",
                        user_current_level=3.0,
                        target_required_level=float(course.target_level),
                        gap_value=0.0,
                        gap_severity="Low",
                        priority_rank=0,
                        recommendation_reason=f"Foundational NSSTA curriculum for official statistical capacity building."
                    ))
                    if len(final_recs) >= limit:
                        break

        # Assign 1-indexed priority rank
        for idx, rec in enumerate(final_recs):
            rec.priority_rank = idx + 1

        return final_recs
