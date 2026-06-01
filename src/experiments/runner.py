from __future__ import annotations
from pathlib import Path

from src.experiments.batadal_experiment import BATADALExperiment
from src.experiments.skab_experiment import SKABExperiment
from src.utils.config import load_yaml_config


class ExperimentRunner:
    """Top-level experiment orchestrator."""

    def __init__(self, config_path: str | Path = Path("configs")) -> None:
        self.config_root = Path(config_path)

    def run(self) -> None:
        skab_config = load_yaml_config(self.config_root / "skab.yaml")
        batadal_config = load_yaml_config(self.config_root / "batadal.yaml")

        print("🚀 Running SKAB experiment")
        SKABExperiment(skab_config).run()

        print("\n🚀 Running BATADAL experiment")
        BATADALExperiment(batadal_config).run()
