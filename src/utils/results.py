from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def flatten_experiment_results(results: dict[str, dict[str, list[float]]]) -> pd.DataFrame:
    """Flatten nested scenario metrics into a DataFrame."""
    rows: list[dict[str, Any]] = []
    for scenario, metric_lists in results.items():
        for metric_key, values in metric_lists.items():
            if "_" not in metric_key:
                continue
            model_name, metric_name = metric_key.rsplit("_", 1)
            rows.append(
                {
                    "scenario": scenario,
                    "model": model_name,
                    "metric": metric_name,
                    "value": float(values[0]) if len(values) == 1 else float(sum(values) / len(values)),
                    "folds": len(values),
                }
            )
    return pd.DataFrame(rows)


def save_results_to_csv(
    results: dict[str, dict[str, list[float]]],
    results_root: Path,
    experiment_name: str,
) -> None:
    """Save experiment results to CSV files per scenario and overall."""
    results_root.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict[str, Any]] = []
    for scenario, metric_lists in results.items():
        for metric_key, values in metric_lists.items():
            if "_" not in metric_key:
                continue
            model_name, metric_name = metric_key.rsplit("_", 1)
            summary_rows.append(
                {
                    "scenario": scenario,
                    "model": model_name,
                    "metric": metric_name,
                    "mean": float(sum(values) / len(values)) if values else 0.0,
                    "min": float(min(values)) if values else 0.0,
                    "max": float(max(values)) if values else 0.0,
                    "folds": len(values),
                }
            )

    summary_df = pd.DataFrame(summary_rows)
    full_path = results_root / f"{experiment_name}_results_summary.csv"
    summary_df.to_csv(full_path, index=False)

    for scenario, scenario_df in summary_df.groupby("scenario"):
        scenario_path = results_root / f"{experiment_name}_{scenario}_results.csv"
        scenario_df.to_csv(scenario_path, index=False)
