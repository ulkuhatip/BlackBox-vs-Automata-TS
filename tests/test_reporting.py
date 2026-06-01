import json
from pathlib import Path

import pandas as pd

from src.utils.reporting import export_results_to_json, generate_comparison_matrix, save_comparison_matrices
from src.utils.benchmark import generate_benchmark_report


def test_export_results_to_json_creates_valid_json(tmp_path: Path) -> None:
    results = {
        "original": {
            "automata_accuracy": [0.85, 0.90],
            "automata_f1": [0.80, 0.88],
            "lstm_accuracy": [0.88, 0.92],
            "lstm_f1": [0.86, 0.90],
        },
        "gaussian_noise": {
            "automata_accuracy": [0.75, 0.80],
            "automata_f1": [0.70, 0.78],
        },
    }

    export_results_to_json(results, tmp_path, "test_experiment")

    json_path = tmp_path / "test_experiment_results.json"
    assert json_path.exists()

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["experiment"] == "test_experiment"
    assert "original" in data["scenarios"]
    assert "automata" in data["scenarios"]["original"]["models"]
    assert "accuracy" in data["scenarios"]["original"]["models"]["automata"]
    assert data["scenarios"]["original"]["models"]["automata"]["accuracy"]["mean"] == 0.875


def test_generate_comparison_matrix_creates_dataframe() -> None:
    results = {
        "original": {
            "automata_f1": [0.85, 0.90],
            "lstm_f1": [0.88, 0.92],
        },
        "noisy": {
            "automata_f1": [0.75, 0.80],
            "lstm_f1": [0.78, 0.82],
        },
    }

    matrix = generate_comparison_matrix(results, metric="f1")

    assert not matrix.empty
    assert "automata" in matrix.columns
    assert "lstm" in matrix.columns
    assert len(matrix) == 2


def test_save_comparison_matrices_creates_csv_files(tmp_path: Path) -> None:
    results = {
        "original": {
            "automata_accuracy": [0.85, 0.90],
            "lstm_accuracy": [0.88, 0.92],
        }
    }

    save_comparison_matrices(results, tmp_path, "test")

    csv_files = list(tmp_path.glob("test_*_comparison_matrix.csv"))
    assert len(csv_files) > 0
