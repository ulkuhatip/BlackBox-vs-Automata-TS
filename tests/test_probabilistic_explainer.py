from __future__ import annotations

import pytest
from src.explainability.probabilistic_explainer import (
    path_probability,
    log_path_probability,
    classify_probability,
    explain_decision,
    explain_sequence,
    format_explanation_text,
    compute_sequence_statistics,
)


# ──────────────────────────────────────────────
# path_probability
# ──────────────────────────────────────────────

def test_path_probability_single_value() -> None:
    assert path_probability([0.72]) == pytest.approx(0.72)


def test_path_probability_multiple_values() -> None:
    result = path_probability([0.72, 0.15])
    assert result == pytest.approx(0.72 * 0.15)


def test_path_probability_empty_returns_zero() -> None:
    assert path_probability([]) == 0.0


def test_path_probability_zero_in_chain_returns_zero() -> None:
    assert path_probability([0.5, 0.0, 0.8]) == 0.0


def test_path_probability_all_ones() -> None:
    assert path_probability([1.0, 1.0, 1.0]) == pytest.approx(1.0)


def test_path_probability_negative_returns_zero() -> None:
    assert path_probability([0.5, -0.1]) == 0.0


# ──────────────────────────────────────────────
# log_path_probability
# ──────────────────────────────────────────────

def test_log_path_probability_empty_returns_neg_inf() -> None:
    import math
    assert log_path_probability([]) == float("-inf")


def test_log_path_probability_zero_returns_neg_inf() -> None:
    import math
    result = log_path_probability([0.5, 0.0])
    assert result == float("-inf")


def test_log_path_probability_consistent_with_path_probability() -> None:
    import math
    transitions = [0.72, 0.15]
    log_result = log_path_probability(transitions)
    direct_result = path_probability(transitions)
    assert math.exp(log_result) == pytest.approx(direct_result, rel=1e-6)


# ──────────────────────────────────────────────
# classify_probability
# ──────────────────────────────────────────────

def test_classify_probability_low_is_anomaly() -> None:
    result = classify_probability(0.05, anomaly_threshold=0.15)
    assert result["decision"] == "anomaly"
    assert result["is_anomaly"] is True


def test_classify_probability_high_is_normal() -> None:
    result = classify_probability(0.8, anomaly_threshold=0.15)
    assert result["decision"] == "normal"
    assert result["is_anomaly"] is False


def test_classify_probability_zero_is_anomaly() -> None:
    result = classify_probability(0.0)
    assert result["decision"] == "anomaly"
    assert result["confidence_level"] == "Very Low"


def test_classify_probability_above_threshold_is_normal() -> None:
    result = classify_probability(0.5, anomaly_threshold=0.15)
    assert result["decision"] == "normal"


def test_classify_probability_returns_required_keys() -> None:
    result = classify_probability(0.3)
    assert "decision" in result
    assert "probability" in result
    assert "confidence_level" in result
    assert "is_anomaly" in result


# ──────────────────────────────────────────────
# explain_decision
# ──────────────────────────────────────────────

def test_explain_decision_seen_pattern() -> None:
    vocab = {"abc", "aab", "bcc"}
    transitions = {("aab", "abc"): 0.72, ("abc", "bcc"): 0.15}
    result = explain_decision(
        time_step=5,
        previous_state="aab",
        incoming_pattern="abc",
        vocabulary=vocab,
        transition_probs=transitions,
    )
    assert result["status"] == "seen"
    assert result["time_step"] == 5
    assert result["previous_state"] == "aab"
    assert result["incoming_pattern"] == "abc"
    assert result["nearest_pattern"] is None


def test_explain_decision_unseen_pattern() -> None:
    vocab = {"abc", "aab", "bcc"}
    transitions = {("aab", "abc"): 0.72}
    result = explain_decision(
        time_step=5,
        previous_state="aab",
        incoming_pattern="adc",
        vocabulary=vocab,
        transition_probs=transitions,
        nearest_pattern="abc",
        edit_distance=1,
    )
    assert result["status"] == "unseen"
    assert result["nearest_pattern"] == "abc"
    assert result["edit_distance"] == 1


def test_explain_decision_low_probability_is_anomaly() -> None:
    vocab = {"aab", "abc"}
    transitions = {("aab", "abc"): 0.05}
    result = explain_decision(
        time_step=1,
        previous_state="aab",
        incoming_pattern="abc",
        vocabulary=vocab,
        transition_probs=transitions,
        anomaly_threshold=0.15,
    )
    assert result["is_anomaly"] is True


def test_explain_decision_high_probability_is_normal() -> None:
    vocab = {"aab", "abc"}
    transitions = {("aab", "abc"): 0.9}
    result = explain_decision(
        time_step=1,
        previous_state="aab",
        incoming_pattern="abc",
        vocabulary=vocab,
        transition_probs=transitions,
        anomaly_threshold=0.15,
    )
    assert result["is_anomaly"] is False


# ──────────────────────────────────────────────
# explain_sequence
# ──────────────────────────────────────────────

def test_explain_sequence_length() -> None:
    patterns = ["aab", "abc", "bcc", "aab"]
    vocab = {"aab", "abc", "bcc"}
    transitions = {
        ("aab", "abc"): 0.72,
        ("abc", "bcc"): 0.15,
        ("bcc", "aab"): 0.60,
    }
    explanations = explain_sequence(patterns, vocab, transitions)
    assert len(explanations) == len(patterns) - 1


def test_explain_sequence_empty_patterns() -> None:
    explanations = explain_sequence([], set(), {})
    assert explanations == []


def test_explain_sequence_single_pattern() -> None:
    explanations = explain_sequence(["aab"], {"aab"}, {})
    assert explanations == []


def test_explain_sequence_time_steps_correct() -> None:
    patterns = ["aab", "abc", "bcc"]
    vocab = {"aab", "abc", "bcc"}
    transitions = {("aab", "abc"): 0.5, ("abc", "bcc"): 0.5}
    explanations = explain_sequence(patterns, vocab, transitions, start_time_step=10)
    assert explanations[0]["time_step"] == 11
    assert explanations[1]["time_step"] == 12


# ──────────────────────────────────────────────
# format_explanation_text
# ──────────────────────────────────────────────

def test_format_explanation_text_contains_required_fields() -> None:
    explanation = {
        "time_step": 5,
        "previous_state": "aab",
        "incoming_pattern": "adc",
        "status": "unseen",
        "nearest_pattern": "abc",
        "edit_distance": 1,
        "transitions": {"aab -> abc": 0.72},
        "path_probability": 0.108,
        "decision": "anomaly",
        "is_anomaly": True,
        "confidence_level": "Low",
        "confidence_score": 0.108,
    }
    text = format_explanation_text(explanation)
    assert "[SYSTEM DECISION]" in text
    assert "Time Step" in text
    assert "aab" in text
    assert "adc" in text
    assert "Unseen" in text
    assert "ANOMALY" in text


def test_format_explanation_text_seen_pattern() -> None:
    explanation = {
        "time_step": 3,
        "previous_state": "abc",
        "incoming_pattern": "bcc",
        "status": "seen",
        "nearest_pattern": None,
        "edit_distance": None,
        "transitions": {"abc -> bcc": 0.8},
        "path_probability": 0.8,
        "decision": "normal",
        "is_anomaly": False,
        "confidence_level": "High",
        "confidence_score": 0.8,
    }
    text = format_explanation_text(explanation)
    assert "NORMAL" in text
    assert "Seen" in text


# ──────────────────────────────────────────────
# compute_sequence_statistics
# ──────────────────────────────────────────────

def test_compute_sequence_statistics_empty() -> None:
    result = compute_sequence_statistics([])
    assert result["n_steps"] == 0
    assert result["n_anomalies"] == 0


def test_compute_sequence_statistics_correct_counts() -> None:
    explanations = [
        {"is_anomaly": True, "status": "unseen", "path_probability": 0.05},
        {"is_anomaly": False, "status": "seen", "path_probability": 0.80},
        {"is_anomaly": True, "status": "seen", "path_probability": 0.10},
    ]
    result = compute_sequence_statistics(explanations)
    assert result["n_steps"] == 3
    assert result["n_anomalies"] == 2
    assert result["n_unseen"] == 1
    assert result["anomaly_rate"] == pytest.approx(2 / 3)


def test_compute_sequence_statistics_mean_probability() -> None:
    explanations = [
        {"is_anomaly": False, "status": "seen", "path_probability": 0.6},
        {"is_anomaly": False, "status": "seen", "path_probability": 0.8},
    ]
    result = compute_sequence_statistics(explanations)
    assert result["mean_probability"] == pytest.approx(0.7)