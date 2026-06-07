from __future__ import annotations

import pytest
import numpy as np

from src.evaluation.statistical_tests import (
    wilcoxon_test,
    mcnemar_test,
    compare_models,
    summarize_fold_results,
    compare_all_models,
)


# ──────────────────────────────────────────────
# Wilcoxon Testleri
# ──────────────────────────────────────────────

def test_wilcoxon_returns_dict_with_required_keys() -> None:
    result = wilcoxon_test([0.8, 0.85, 0.9], [0.7, 0.75, 0.8])
    assert "test" in result
    assert "p_value" in result
    assert "significant" in result
    assert "statistic" in result
    assert "interpretation" in result


def test_wilcoxon_identical_scores_not_significant() -> None:
    scores = [0.8, 0.8, 0.8, 0.8, 0.8]
    result = wilcoxon_test(scores, scores)
    assert result["significant"] is False


def test_wilcoxon_clearly_different_scores() -> None:
    a = [0.9, 0.91, 0.92, 0.93, 0.94]
    b = [0.1, 0.11, 0.12, 0.13, 0.14]
    result = wilcoxon_test(a, b)
    assert result["p_value"] < 0.05
    assert result["significant"] is True


def test_wilcoxon_unequal_length_raises() -> None:
    with pytest.raises(ValueError, match="eşit uzunlukta"):
        wilcoxon_test([0.8, 0.9], [0.7])


def test_wilcoxon_single_element_returns_safely() -> None:
    result = wilcoxon_test([0.8], [0.7])
    assert result["significant"] is False


def test_wilcoxon_p_value_between_0_and_1() -> None:
    result = wilcoxon_test([0.8, 0.85, 0.9, 0.82, 0.88], [0.75, 0.80, 0.85, 0.77, 0.83])
    p = result["p_value"]
    assert 0.0 <= p <= 1.0


# ──────────────────────────────────────────────
# McNemar Testleri
# ──────────────────────────────────────────────

def test_mcnemar_returns_dict_with_required_keys() -> None:
    y_true = [0, 1, 0, 1, 0]
    y_pred_a = [0, 1, 0, 0, 0]
    y_pred_b = [0, 0, 0, 1, 0]
    result = mcnemar_test(y_true, y_pred_a, y_pred_b)
    assert "test" in result
    assert "p_value" in result
    assert "significant" in result
    assert "n01" in result
    assert "n10" in result


def test_mcnemar_identical_predictions_not_significant() -> None:
    y_true = [0, 1, 0, 1, 1]
    y_pred = [0, 1, 0, 0, 1]
    result = mcnemar_test(y_true, y_pred, y_pred)
    assert result["significant"] is False
    assert result["n01"] == 0
    assert result["n10"] == 0


def test_mcnemar_unequal_length_raises() -> None:
    with pytest.raises(ValueError):
        mcnemar_test([0, 1], [0, 1], [0])


def test_mcnemar_p_value_between_0_and_1() -> None:
    y_true =   [0, 1, 0, 1, 0, 1, 0, 1]
    y_pred_a = [0, 1, 0, 0, 0, 1, 0, 0]
    y_pred_b = [0, 0, 0, 1, 0, 0, 0, 1]
    result = mcnemar_test(y_true, y_pred_a, y_pred_b)
    assert 0.0 <= result["p_value"] <= 1.0


def test_mcnemar_counts_correct() -> None:
    # A yanlış B doğru = n01, A doğru B yanlış = n10
    y_true =   [1, 1, 1, 1]
    y_pred_a = [0, 0, 1, 1]  # ilk ikisinde yanlış
    y_pred_b = [1, 1, 0, 0]  # son ikisinde yanlış
    result = mcnemar_test(y_true, y_pred_a, y_pred_b)
    assert result["n01"] == 2  # A yanlış B doğru
    assert result["n10"] == 2  # A doğru B yanlış


# ──────────────────────────────────────────────
# Compare Models Testleri
# ──────────────────────────────────────────────

def test_compare_models_returns_mean_and_std() -> None:
    a = [0.8, 0.85, 0.9, 0.82, 0.88]
    b = [0.7, 0.75, 0.8, 0.72, 0.78]
    result = compare_models(a, b, "LSTM", "Automata")
    assert "mean_a" in result
    assert "mean_b" in result
    assert "std_a" in result
    assert "std_b" in result
    assert result["model_a"] == "LSTM"
    assert result["model_b"] == "Automata"


def test_compare_models_mean_diff_correct() -> None:
    a = [0.9, 0.9, 0.9]
    b = [0.8, 0.8, 0.8]
    result = compare_models(a, b)
    assert abs(result["mean_diff"] - 0.1) < 1e-9


# ──────────────────────────────────────────────
# Summarize Fold Results Testleri
# ──────────────────────────────────────────────

def test_summarize_fold_results_correct_mean() -> None:
    scores = [0.8, 0.9, 0.85]
    result = summarize_fold_results(scores, "lstm", "f1")
    assert abs(result["mean"] - 0.85) < 1e-9


def test_summarize_fold_results_summary_format() -> None:
    scores = [0.8, 0.9]
    result = summarize_fold_results(scores)
    assert "±" in result["summary"]


def test_summarize_fold_results_empty_scores() -> None:
    result = summarize_fold_results([], "model", "f1")
    assert result["mean"] == 0.0
    assert result["n_folds"] == 0


def test_summarize_fold_results_single_score() -> None:
    result = summarize_fold_results([0.75], "gru", "f1")
    assert result["mean"] == 0.75
    assert result["n_folds"] == 1


# ──────────────────────────────────────────────
# Compare All Models Testleri
# ──────────────────────────────────────────────

def test_compare_all_models_pairwise() -> None:
    results = {
        "lstm": [0.8, 0.85, 0.9],
        "gru": [0.75, 0.80, 0.85],
        "automata": [0.7, 0.72, 0.75],
    }
    comparisons = compare_all_models(results)
    # 3 model → 3 çift karşılaştırma
    assert len(comparisons) == 3


def test_compare_all_models_with_baseline() -> None:
    results = {
        "lstm": [0.8, 0.85, 0.9],
        "gru": [0.75, 0.80, 0.85],
        "automata": [0.7, 0.72, 0.75],
    }
    comparisons = compare_all_models(results, baseline_model="lstm")
    # Baseline ile 2 karşılaştırma
    assert len(comparisons) == 2
    assert all(c["model_a"] == "lstm" for c in comparisons)


def test_compare_all_models_empty_results() -> None:
    comparisons = compare_all_models({})
    assert comparisons == []