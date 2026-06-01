from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def export_results_to_json(
    results: dict[str, dict[str, list[float]]],
    results_root: Path,
    experiment_name: str,
) -> None:
    """
    Export experiment results to JSON format with hierarchical structure.
    
    JSON Structure:
    {
        "experiment": "skab",
        "scenarios": {
            "original": {
                "models": {
                    "automata": {"accuracy": [...], "precision": [...], ...},
                    "lstm": {...},
                    ...
                }
            },
            ...
        }
    }
    """
    results_root.mkdir(parents=True, exist_ok=True)
    
    json_structure: dict[str, Any] = {
        "experiment": experiment_name,
        "scenarios": {},
    }
    
    for scenario, metric_lists in results.items():
        models_data: dict[str, dict[str, Any]] = {}
        
        for metric_key, values in metric_lists.items():
            if "_" not in metric_key:
                continue
            
            model_name, metric_name = metric_key.rsplit("_", 1)
            
            if model_name not in models_data:
                models_data[model_name] = {}
            
            models_data[model_name][metric_name] = {
                "values": [float(v) for v in values],
                "mean": float(sum(values) / len(values)) if values else 0.0,
                "min": float(min(values)) if values else 0.0,
                "max": float(max(values)) if values else 0.0,
                "folds": len(values),
            }
        
        json_structure["scenarios"][scenario] = {"models": models_data}
    
    json_path = results_root / f"{experiment_name}_results.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(json_structure, f, indent=2, ensure_ascii=False)


def generate_comparison_matrix(
    results: dict[str, dict[str, list[float]]],
    metric: str = "f1",
) -> pd.DataFrame:
    """Generate a model comparison matrix for a specific metric across scenarios."""
    matrix_data: dict[str, dict[str, float]] = {}
    
    for scenario, metric_lists in results.items():
        for metric_key, values in metric_lists.items():
            if "_" not in metric_key:
                continue
            
            model_name, metric_name = metric_key.rsplit("_", 1)
            
            if metric_name != metric:
                continue
            
            if scenario not in matrix_data:
                matrix_data[scenario] = {}
            
            mean_value = float(sum(values) / len(values)) if values else 0.0
            matrix_data[scenario][model_name] = mean_value
    
    if not matrix_data:
        return pd.DataFrame()
    
    return pd.DataFrame(matrix_data).T


def save_comparison_matrices(
    results: dict[str, dict[str, list[float]]],
    results_root: Path,
    experiment_name: str,
) -> None:
    """Save comparison matrices for all metrics."""
    results_root.mkdir(parents=True, exist_ok=True)
    
    metrics = set()
    for metric_lists in results.values():
        for metric_key in metric_lists.keys():
            if "_" in metric_key:
                _, metric_name = metric_key.rsplit("_", 1)
                metrics.add(metric_name)
    
    for metric in metrics:
        matrix = generate_comparison_matrix(results, metric=metric)
        if not matrix.empty:
            matrix_path = results_root / f"{experiment_name}_{metric}_comparison_matrix.csv"
            matrix.to_csv(matrix_path)
