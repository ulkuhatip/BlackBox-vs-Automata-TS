from __future__ import annotations
from collections import defaultdict
from statistics import mean
from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split

from src.data.preprocess import PreprocessingPipeline
from src.data.skab_loader import SKABLoader
from src.data.splitters import split_skab_groups
from src.evaluation.metrics import compute_classification_metrics
from src.features.noise import add_gaussian_noise
from src.features.windowing import windows_to_sax_patterns
from src.models.automata.automaton import ProbabilisticAutomaton
from src.data.unseen_generator import (
    create_unseen_scenario,
    extract_sax_vocabulary,
)


class SKABExperiment:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.dataset_config = config["dataset"]
        self.preprocessing_config = config["preprocessing"]
        self.automata_config = config["automata"]
        self.experiment_config = config["experiment"]

    def run(self) -> None:
        loader = SKABLoader(
            raw_root=self.dataset_config["raw_root"],
            processed_root=self.dataset_config["processed_root"],
            groups=self.dataset_config["groups"],
            delimiter=self.dataset_config.get("delimiter", ";"),
        )

        combined_path = loader.save_combined("combined.csv")
        dataset = pd.read_csv(combined_path)

        folds = split_skab_groups(
            dataset=dataset,
            group_column=self.dataset_config["split"]["group_column"],
            target_column=self.dataset_config["target_column"],
            n_splits=self.dataset_config["split"]["n_splits"],
        )

        results: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
        for fold_index, (train_df, test_df) in enumerate(folds, start=1):
            train_df, validation_df = self._train_validation_split(train_df)
            pipeline = PreprocessingPipeline(
                scaler_type=self.preprocessing_config["scaler"],
                pca_components=self.preprocessing_config["pca_components"],
            )
            artifacts = pipeline.fit_transform(train_df, validation_df, test_df)

            for scenario in self.experiment_config["scenarios"]:
                metrics = self._run_automata_scenario(artifacts, scenario)
                for key, value in metrics.items():
                    results[scenario][key].append(value)

            print(f"✅ SKAB fold {fold_index} completed.")

        print("\n=== SKAB summary ===")
        for scenario, metric_lists in results.items():
            summary = {
                metric: float(mean(values)) if values else 0.0
                for metric, values in metric_lists.items()
            }
            print(f"Scenario: {scenario} → {summary}")

    def _train_validation_split(self, train_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame | None]:
        if len(train_df) < 10:
            return train_df, None

        return train_test_split(
            train_df,
            test_size=0.2,
            stratify=train_df[self.dataset_config["target_column"]],
            random_state=self.experiment_config["seeds"][0],
        )

    def _run_automata_scenario(
        self,
        artifacts: Any,
        scenario: str,
    ) -> dict[str, float]:
        test_df = artifacts.test.copy()
        if scenario == "gaussian_noise":
            test_df = add_gaussian_noise(test_df, seed=self.experiment_config["seeds"][0])

        automaton = ProbabilisticAutomaton(
            window_size=self.automata_config["window_size"],
            alphabet_size=self.automata_config["alphabet_size"],
            anomaly_threshold=0.15,
        )
        automaton.fit(artifacts.train["PC1"].tolist())

        if scenario == "unseen":
            training_patterns = windows_to_sax_patterns(
                artifacts.train["PC1"].tolist(),
                self.automata_config["window_size"],
                self.automata_config["alphabet_size"],
            )
            vocabulary = extract_sax_vocabulary(training_patterns)
            patterns, _ = create_unseen_scenario(
                series=test_df["PC1"].tolist(),
                sax_vocabulary=vocabulary,
                alphabet_size=self.automata_config["alphabet_size"],
                window_size=self.automata_config["window_size"],
                seed=self.experiment_config["seeds"][0],
            )
        else:
            patterns = windows_to_sax_patterns(
                test_df["PC1"].tolist(),
                self.automata_config["window_size"],
                self.automata_config["alphabet_size"],
            )

        y_true = test_df[self.dataset_config["target_column"]].iloc[self.automata_config["window_size"] - 1 :].to_numpy()
        y_pred = automaton.predict(patterns)

        return compute_classification_metrics(y_true, y_pred)
