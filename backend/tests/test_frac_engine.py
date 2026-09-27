import pytest

def test_frac_competency_gap_and_radar():
    from backend.app.services.frac_engine import (
        calculate_competency_gaps,
        calculate_readiness_index,
        format_radar_chart_data,
        evaluate_diagnostic_test,
    )
    from backend.app.schemas.competency import BenchmarkItem, ScoreItem

    # Setup test benchmarks for a statistical role
    benchmarks = [
        BenchmarkItem(competency_code="COMP_SAMPLING", competency_name="Survey Sampling", required_level=4.0, weight=1.5),
        BenchmarkItem(competency_code="COMP_PLFS", competency_name="Labour Force Survey", required_level=4.0, weight=1.5),
        BenchmarkItem(competency_code="COMP_R_STAT", competency_name="R Programming", required_level=3.0, weight=1.0),
        BenchmarkItem(competency_code="COMP_ETHICS", competency_name="Data Ethics", required_level=5.0, weight=1.0),
    ]

    # Current user scores
    scores = [
        ScoreItem(competency_code="COMP_SAMPLING", current_level=2.5),  # Gap: 1.5
        ScoreItem(competency_code="COMP_PLFS", current_level=4.0),      # Gap: 0.0 (Met)
        ScoreItem(competency_code="COMP_R_STAT", current_level=1.0),    # Gap: 2.0 (High Deficit!)
        ScoreItem(competency_code="COMP_ETHICS", current_level=5.0),    # Gap: 0.0 (Met)
    ]

    # 1. Test Gap Calculation
    gaps = calculate_competency_gaps(benchmarks, scores)
    assert len(gaps) == 4
    # Gaps should be sorted descending by priority (gap * weight)
    # COMP_SAMPLING: gap 1.5 * weight 1.5 = 2.25
    # COMP_R_STAT: gap 2.0 * weight 1.0 = 2.0
    assert gaps[0].competency_code == "COMP_SAMPLING"
    assert gaps[0].gap == 1.5
    assert gaps[0].deficit_level == "Medium"
    
    assert gaps[1].competency_code == "COMP_R_STAT"
    assert gaps[1].gap == 2.0
    assert gaps[1].deficit_level == "High"
    
    # 2. Test Cadre Readiness Index (Omega)
    # Omega = sum(weight * min(1.0, current/target)) / sum(weight)
    # Sampling: 1.5 * (2.5/4.0) = 1.5 * 0.625 = 0.9375
    # PLFS: 1.5 * (4.0/4.0) = 1.5
    # R: 1.0 * (1.0/3.0) = 0.3333
    # Ethics: 1.0 * (5.0/5.0) = 1.0
    # Sum weighted = 0.9375 + 1.5 + 0.3333 + 1.0 = 3.7708
    # Total weight = 1.5 + 1.5 + 1.0 + 1.0 = 5.0
    # Index = 3.7708 / 5.0 = ~0.754 (75.4%)
    readiness = calculate_readiness_index(benchmarks, scores)
    assert 70.0 <= readiness <= 80.0

    # 3. Test Radar Chart Data Structure (compatible with Recharts Radar)
    radar_data = format_radar_chart_data(benchmarks, scores)
    assert len(radar_data) == 4
    for item in radar_data:
        assert hasattr(item, "competency")
        assert hasattr(item, "required")
        assert hasattr(item, "current")
        assert hasattr(item, "gap")
        assert 0 <= item.current <= 5.0
        assert 0 <= item.required <= 5.0

    # 4. Test Diagnostic Assessment Scoring
    diagnostic_answers = {
        "q1": {"competency_code": "COMP_SAMPLING", "is_correct": True},
        "q2": {"competency_code": "COMP_SAMPLING", "is_correct": False},
        "q3": {"competency_code": "COMP_R_STAT", "is_correct": True},
    }
    diag_scores = evaluate_diagnostic_test(diagnostic_answers)
    assert "COMP_SAMPLING" in diag_scores
    # 1 of 2 correct = 50% -> mapped to 2.5 on 1-5 scale
    assert 2.0 <= diag_scores["COMP_SAMPLING"] <= 3.0
    assert diag_scores["COMP_R_STAT"] >= 4.0
