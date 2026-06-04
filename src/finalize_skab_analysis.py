from __future__ import annotations

import json
import re
from pathlib import Path
from statistics import mean, stdev
from typing import Any


RESULTS_ROOT = Path("results/skab")
STAGE2_PATTERN = re.compile(r"stage2_w(?P<window>\d+)_a(?P<alphabet>\d+)_results\.json$")


def _load_stage2_results(results_root: Path) -> list[dict[str, Any]]:
    analysis: list[dict[str, Any]] = []

    for json_path in sorted(results_root.glob("stage2_w*_a*_results.json")):
        match = STAGE2_PATTERN.fullmatch(json_path.name)
        if match is None:
            continue

        payload = json.loads(json_path.read_text(encoding="utf-8"))
        combo_analysis = {
            "window_size": int(match.group("window")),
            "alphabet_size": int(match.group("alphabet")),
            "scenarios": {},
        }

        for scenario, scenario_payload in payload.get("scenarios", {}).items():
            scenario_metrics: dict[str, dict[str, float]] = {}
            models = scenario_payload.get("models", {})

            for model_name, metrics_payload in models.items():
                for metric_name, values_payload in metrics_payload.items():
                    values = [float(value) for value in values_payload.get("values", [])]
                    if not values:
                        continue

                    composite_metric = f"{model_name}_{metric_name}"
                    scenario_metrics[composite_metric] = {
                        "mean": float(mean(values)),
                        "std": float(stdev(values)) if len(values) > 1 else 0.0,
                        "min": float(min(values)),
                        "max": float(max(values)),
                    }

            combo_analysis["scenarios"][scenario] = scenario_metrics

        analysis.append(combo_analysis)

    return analysis


def _save_analysis_outputs(analysis: list[dict[str, Any]], results_root: Path) -> None:
    analysis_file = results_root / "parameter_analysis.json"
    analysis_file.write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report_file = results_root / "parameter_analysis_report.md"
    with report_file.open("w", encoding="utf-8") as f:
        f.write("# SKAB Parameter Analysis Report\n\n")
        f.write("## Parameter Grid Search Results\n\n")
        f.write("16 combinations x 5 folds = 80 model evaluations\n\n")

        for combo in analysis:
            window_size = combo["window_size"]
            alphabet_size = combo["alphabet_size"]
            f.write(f"### Window Size={window_size}, Alphabet Size={alphabet_size}\n\n")

            for scenario, metrics in combo["scenarios"].items():
                f.write(f"#### Scenario: {scenario}\n")
                f.write("| Metric | Mean | Std | Min | Max |\n")
                f.write("|--------|------|-----|-----|-----|\n")

                for metric_name, values in metrics.items():
                    f.write(
                        f"| {metric_name} | {values['mean']:.4f} | {values['std']:.4f} | "
                        f"{values['min']:.4f} | {values['max']:.4f} |\n"
                    )

                f.write("\n")


def main() -> None:
    if not RESULTS_ROOT.exists():
        raise FileNotFoundError(f"Missing results directory: {RESULTS_ROOT}")

    analysis = _load_stage2_results(RESULTS_ROOT)
    if not analysis:
        raise FileNotFoundError("No saved SKAB stage2 result JSON files were found.")

    _save_analysis_outputs(analysis, RESULTS_ROOT)
    print(f"Rebuilt SKAB analysis from {len(analysis)} saved stage2 result files.")
    print(f"Saved: {RESULTS_ROOT / 'parameter_analysis.json'}")
    print(f"Saved: {RESULTS_ROOT / 'parameter_analysis_report.md'}")


if __name__ == "__main__":
    main()
