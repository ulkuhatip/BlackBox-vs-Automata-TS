from __future__ import annotations

import copy
import os
from pathlib import Path

from src.experiments.batadal_experiment import BATADALExperiment
from src.experiments.skab_experiment import SKABExperiment
from src.utils.config import load_yaml_config


class ExperimentRunner:
    """Top-level experiment orchestrator."""

    def __init__(self, config_path: str | Path = Path("configs")) -> None:
        self.config_root = Path(config_path)

    def _apply_runtime_overrides(self, config: dict, dataset_name: str) -> dict:
        runtime_config = copy.deepcopy(config)

        debug_enabled = os.getenv("BBATS_DEBUG", "").lower() in {"1", "true", "yes", "on"}
        if not debug_enabled:
            return runtime_config

        debug_scenarios = os.getenv("BBATS_DEBUG_SCENARIOS", "original")
        scenarios = [item.strip() for item in debug_scenarios.split(",") if item.strip()]
        if scenarios:
            runtime_config["experiment"]["scenarios"] = scenarios

        runtime_config["experiment"]["seeds"] = runtime_config["experiment"]["seeds"][:1]
        runtime_config["experiment"]["stage1_only"] = True
        runtime_config["deep_learning"]["epochs"] = min(
            runtime_config["deep_learning"]["epochs"],
            int(os.getenv("BBATS_DEBUG_EPOCHS", "2")),
        )
        runtime_config["deep_learning"]["early_stopping_patience"] = min(
            runtime_config["deep_learning"]["early_stopping_patience"],
            1,
        )

        debug_models = os.getenv("BBATS_DEBUG_MODELS", "")
        if debug_models.strip():
            runtime_config["deep_learning"]["enabled_models"] = [
                item.strip() for item in debug_models.split(",") if item.strip()
            ]

        if dataset_name == "skab":
            runtime_config["dataset"]["split"]["n_splits"] = max(
                2,
                int(os.getenv("BBATS_DEBUG_SKAB_SPLITS", "2")),
            )
            runtime_config["experiment"]["max_folds"] = max(
                1,
                int(os.getenv("BBATS_DEBUG_MAX_FOLDS", "1")),
            )

        return runtime_config

    def run(self) -> None:
        skab_config = self._apply_runtime_overrides(
            load_yaml_config(self.config_root / "skab.yaml"),
            "skab",
        )
        batadal_config = self._apply_runtime_overrides(
            load_yaml_config(self.config_root / "batadal.yaml"),
            "batadal",
        )

        if os.getenv("BBATS_DEBUG", "").lower() in {"1", "true", "yes", "on"}:
            print("🔧 Debug mode is ON (runtime overrides only, config files unchanged)")

        print("🚀 Running SKAB experiment")
        SKABExperiment(skab_config).run()

        print("\n🚀 Running BATADAL experiment")
        BATADALExperiment(batadal_config).run()
