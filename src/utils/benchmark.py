from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def _dataframe_to_report_table(df: pd.DataFrame) -> str:
    """Render a dataframe for reports without requiring optional markdown deps."""
    try:
        return df.to_markdown(index=False)
    except ImportError:
        return df.to_string(index=False)


def generate_benchmark_report(
    results: dict[str, dict[str, list[float]]],
    results_root: Path,
    experiment_name: str,
) -> None:
    """
    Generate a comprehensive benchmark report comparing all models across scenarios.
    
    Report includes:
    - Overall winner by metric
    - Per-scenario rankings
    - Stability analysis (min/max variance)
    - Cross-scenario performance
    """
    results_root.mkdir(parents=True, exist_ok=True)
    
    report_lines: list[str] = [
        f"# Benchmark Report: {experiment_name.upper()}",
        "",
        "## Summary Statistics",
        "",
    ]
    
    # Collect all results
    all_metrics: dict[str, dict[str, list[float]]] = {}
    for scenario, metric_lists in results.items():
        for metric_key, values in metric_lists.items():
            if "_" not in metric_key:
                continue
            
            model_name, metric_name = metric_key.rsplit("_", 1)
            composite_key = f"{model_name}_{metric_name}"
            
            if composite_key not in all_metrics:
                all_metrics[composite_key] = {}
            all_metrics[composite_key][scenario] = values
    
    # Per-metric analysis
    for metric_key in sorted(all_metrics.keys()):
        metric_data = all_metrics[metric_key]
        report_lines.append(f"### {metric_key.upper()}")
        report_lines.append("")
        
        summary_rows = []
        for scenario, fold_values in sorted(metric_data.items()):
            if not fold_values:
                continue
            mean_val = float(sum(fold_values) / len(fold_values))
            min_val = float(min(fold_values))
            max_val = float(max(fold_values))
            summary_rows.append(
                {
                    "Scenario": scenario,
                    "Mean": f"{mean_val:.4f}",
                    "Min": f"{min_val:.4f}",
                    "Max": f"{max_val:.4f}",
                    "Range": f"{max_val - min_val:.4f}",
                }
            )
        
        if summary_rows:
            summary_df = pd.DataFrame(summary_rows)
            report_lines.append(_dataframe_to_report_table(summary_df))
            report_lines.append("")
    
    # Best performers
    report_lines.append("## Best Performers")
    report_lines.append("")
    
    for scenario in sorted(results.keys()):
        report_lines.append(f"### {scenario.upper()}")
        report_lines.append("")
        
        scenario_best: dict[str, tuple[str, float]] = {}
        for metric_key, fold_values in results[scenario].items():
            if "_" not in metric_key:
                continue
            mean_val = float(sum(fold_values) / len(fold_values)) if fold_values else 0.0
            
            model_name, metric_name = metric_key.rsplit("_", 1)
            
            if metric_name not in scenario_best or mean_val > scenario_best[metric_name][1]:
                scenario_best[metric_name] = (model_name, mean_val)
        
        for metric_name in sorted(scenario_best.keys()):
            model_name, mean_val = scenario_best[metric_name]
            report_lines.append(f"- **{metric_name}**: {model_name} ({mean_val:.4f})")
        report_lines.append("")
    
    report_content = "\n".join(report_lines)
    
    report_path = results_root / f"{experiment_name}_benchmark_report.md"
    report_path.write_text(report_content, encoding="utf-8")
