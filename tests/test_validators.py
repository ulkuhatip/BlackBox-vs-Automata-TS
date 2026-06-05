from __future__ import annotations

import pytest
import pandas as pd
import numpy as np

from src.evaluation.validators import (
    validate_group_split,
    validate_no_data_leakage,
    validate_time_ordered_split,
    validate_fold_results,
    validate_label_distribution,
    validate_pca_fit,
    validate_experiment_config,
)


# ──────────────────────────────────────────────
# validate_group_split
# ──────────────────────────────────────────────

def test_validate_group_split_existing_column() -> None:
    df = pd.DataFrame({"source_file": ["a", "b"], "sensor": [1.0, 2.0]})
    assert validate_group_split(df, "source_file") is True


def test_validate_group_split_missing_column() -> None:
    df = pd.DataFrame({"sensor": [1.0, 2.0]})
    assert validate_group_split(df, "source_file") is False


# ──────────────────────────────────────────────
# validate_no_data_leakage
# ──────────────────────────────────────────────

def test_validate_no_data_leakage_no_overlap() -> None:
    train = ["file1", "file2", "file3"]
    test = ["file4", "file5"]
    assert validate_no_data_leakage(train, test) is True


def test_validate_no_data_leakage_with_overlap_raises() -> None:
    train = ["file1", "file2"]
    test = ["file2", "file3"]
    with pytest.raises(ValueError, match="Veri sızıntısı"):
        validate_no_data_leakage(train, test)


def test_validate_no_data_leakage_empty_sets() -> None:
    assert validate_no_data_leakage([], []) is True


# ──────────────────────────────────────────────
# validate_time_ordered_split
# ──────────────────────────────────────────────

def test_validate_time_ordered_split_valid() -> None:
    df = pd.DataFrame({
        "DATETIME": pd.date_range("2020-01-01", periods=100),
        "sensor": range(100),
    })
    assert validate_time_ordered_split(df, "DATETIME") is True


def test_validate_time_ordered_split_invalid_ratios() -> None:
    df = pd.DataFrame({
        "DATETIME": pd.date_range("2020-01-01", periods=100),
        "sensor": range(100),
    })
    with pytest.raises(ValueError, match="1.0"):
        validate_time_ordered_split(df, "DATETIME", 0.5, 0.3, 0.3)


def test_validate_time_ordered_split_missing_time_column() -> None:
    df = pd.DataFrame({"sensor": range(100)})
    with pytest.raises(ValueError, match="Zaman sütunu"):
        validate_time_ordered_split(df, "DATETIME")


# ──────────────────────────────────────────────
# validate_fold_results
# ──────────────────────────────────────────────

def test_validate_fold_results_valid() -> None:
    folds = [
        {"accuracy": 0.9, "precision": 0.8, "recall": 0.7, "f1": 0.75},
        {"accuracy": 0.85, "precision": 0.75, "recall": 0.65, "f1": 0.70},
    ]
    assert validate_fold_results(folds) is True


def test_validate_fold_results_missing_metric_raises() -> None:
    folds = [{"accuracy": 0.9, "precision": 0.8, "recall": 0.7}]
    with pytest.raises(ValueError, match="f1"):
        validate_fold_results(folds)


def test_validate_fold_results_out_of_range_raises() -> None:
    folds = [{"accuracy": 1.5, "precision": 0.8, "recall": 0.7, "f1": 0.75}]
    with pytest.raises(ValueError, match="geçersiz aralık"):
        validate_fold_results(folds)


def test_validate_fold_results_empty_raises() -> None:
    with pytest.raises(ValueError, match="boş"):
        validate_fold_results([])


# ──────────────────────────────────────────────
# validate_label_distribution
# ──────────────────────────────────────────────

def test_validate_label_distribution_balanced() -> None:
    y = [0] * 50 + [1] * 50
    result = validate_label_distribution(y)
    assert result["n_total"] == 100
    assert result["n_positive"] == 50
    assert result["positive_ratio"] == 0.5
    assert result["is_imbalanced"] is False


def test_validate_label_distribution_imbalanced() -> None:
    y = [0] * 99 + [1] * 1
    result = validate_label_distribution(y, min_positive_ratio=0.05)
    assert result["is_imbalanced"] is True
    assert result["warning"] is not None


def test_validate_label_distribution_empty() -> None:
    result = validate_label_distribution([])
    assert result["n_total"] == 0
    assert result["positive_ratio"] == 0.0


def test_validate_label_distribution_all_negative() -> None:
    y = [0, 0, 0, 0, 0]
    result = validate_label_distribution(y)
    assert result["n_positive"] == 0
    assert result["is_imbalanced"] is True


# ──────────────────────────────────────────────
# validate_pca_fit
# ──────────────────────────────────────────────

def test_validate_pca_fit_valid() -> None:
    train = pd.DataFrame({"PC1": [0.1, 0.2, 0.3], "ATT_FLAG": [0, 1, 0]})
    test = pd.DataFrame({"PC1": [0.15, 0.25], "ATT_FLAG": [0, 1]})
    assert validate_pca_fit(train, test) is True


def test_validate_pca_fit_missing_train_pc1_raises() -> None:
    train = pd.DataFrame({"sensor": [1.0, 2.0]})
    test = pd.DataFrame({"PC1": [0.1, 0.2]})
    with pytest.raises(ValueError, match="Train"):
        validate_pca_fit(train, test)


def test_validate_pca_fit_missing_test_pc1_raises() -> None:
    train = pd.DataFrame({"PC1": [0.1, 0.2]})
    test = pd.DataFrame({"sensor": [1.0, 2.0]})
    with pytest.raises(ValueError, match="Test"):
        validate_pca_fit(train, test)


# ──────────────────────────────────────────────
# validate_experiment_config
# ──────────────────────────────────────────────

def test_validate_experiment_config_valid() -> None:
    config = {
        "dataset": {"name": "skab"},
        "preprocessing": {"scaler": "standard"},
        "deep_learning": {"epochs": 50, "batch_size": 32},
        "automata": {"window_size": 4},
        "experiment": {"seeds": [42, 123]},
    }
    assert validate_experiment_config(config) is True


def test_validate_experiment_config_missing_key_raises() -> None:
    config = {
        "dataset": {},
        "preprocessing": {},
        "deep_learning": {"epochs": 50, "batch_size": 32},
        "experiment": {"seeds": [42]},
    }
    with pytest.raises(ValueError, match="eksik"):
        validate_experiment_config(config)


def test_validate_experiment_config_no_seeds_raises() -> None:
    config = {
        "dataset": {}, "preprocessing": {},
        "deep_learning": {"epochs": 50, "batch_size": 32},
        "automata": {},
        "experiment": {"seeds": []},
    }
    with pytest.raises(ValueError, match="seed"):
        validate_experiment_config(config)


def test_validate_experiment_config_invalid_epochs_raises() -> None:
    config = {
        "dataset": {}, "preprocessing": {},
        "deep_learning": {"epochs": 0, "batch_size": 32},
        "automata": {},
        "experiment": {"seeds": [42]},
    }
    with pytest.raises(ValueError, match="Epoch"):
        validate_experiment_config(config)