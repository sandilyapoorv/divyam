from typing import List, Dict, Any
from backend.app.schemas.competency import (
    BenchmarkItem,
    ScoreItem,
    CompetencyGap,
    RadarAxisItem
)

def calculate_competency_gaps(
    benchmarks: List[BenchmarkItem],
    scores: List[ScoreItem]
) -> List[CompetencyGap]:
    score_map = {s.competency_code: s.current_level for s in scores}
    gaps: List[CompetencyGap] = []

    for bm in benchmarks:
        cur_level = score_map.get(bm.competency_code, 1.0)
        gap_val = max(0.0, round(bm.required_level - cur_level, 2))
        
        if gap_val == 0.0:
            deficit_level = "None"
        elif gap_val <= 0.8:
            deficit_level = "Low"
        elif gap_val <= 1.5:
            deficit_level = "Medium"
        else:
            deficit_level = "High"

        gaps.append(CompetencyGap(
            competency_code=bm.competency_code,
            competency_name=bm.competency_name,
            required_level=bm.required_level,
            current_level=cur_level,
            gap=gap_val,
            deficit_level=deficit_level,
            criticality_weight=bm.weight
        ))

    # Sort descending by priority (gap * weight)
    gaps.sort(key=lambda g: (g.gap * g.criticality_weight, g.gap), reverse=True)
    return gaps

def calculate_readiness_index(
    benchmarks: List[BenchmarkItem],
    scores: List[ScoreItem]
) -> float:
    if not benchmarks:
        return 100.0

    score_map = {s.competency_code: s.current_level for s in scores}
    weighted_achievement = 0.0
    total_weight = 0.0

    for bm in benchmarks:
        cur_level = score_map.get(bm.competency_code, 1.0)
        ratio = min(1.0, cur_level / bm.required_level if bm.required_level > 0 else 1.0)
        weighted_achievement += bm.weight * ratio
        total_weight += bm.weight

    if total_weight == 0:
        return 100.0

    return round((weighted_achievement / total_weight) * 100.0, 1)

def format_radar_chart_data(
    benchmarks: List[BenchmarkItem],
    scores: List[ScoreItem]
) -> List[RadarAxisItem]:
    score_map = {s.competency_code: s.current_level for s in scores}
    radar_items: List[RadarAxisItem] = []

    for bm in benchmarks:
        cur = score_map.get(bm.competency_code, 1.0)
        gap = max(0.0, round(bm.required_level - cur, 2))
        radar_items.append(RadarAxisItem(
            competency=bm.competency_name,
            competency_code=bm.competency_code,
            required=bm.required_level,
            current=cur,
            gap=gap
        ))

    return radar_items

def evaluate_diagnostic_test(answers: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
    """
    Evaluates raw question answers: {q_id: {"competency_code": str, "is_correct": bool}}
    Returns competency scores on a 1.0 to 5.0 scale.
    """
    comp_totals: Dict[str, int] = {}
    comp_correct: Dict[str, int] = {}

    for _, info in answers.items():
        code = info.get("competency_code")
        if not code:
            continue
        comp_totals[code] = comp_totals.get(code, 0) + 1
        if info.get("is_correct", False):
            comp_correct[code] = comp_correct.get(code, 0) + 1

    scores: Dict[str, float] = {}
    for code, total in comp_totals.items():
        correct = comp_correct.get(code, 0)
        ratio = correct / total if total > 0 else 0.0
        # Map 0.0 - 1.0 ratio to 1.0 - 5.0 scale
        score_val = round(1.0 + (ratio * 4.0), 1)
        scores[code] = score_val

    return scores
