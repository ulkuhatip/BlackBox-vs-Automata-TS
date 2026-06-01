from __future__ import annotations
from collections import defaultdict
from statistics import mean
from typing import Any

import pandas as pd

from src.data.batadal_loader import BATADALLoader
from src.data.preprocess import PreprocessingPipeline
from src.data.splitters import split_batadal_time
from src.evaluation.metrics import compute_classification_metrics
from src.features.noise import add_gaussian_noise, create_numeric_unseen_scenario
from src.features.windowing import (
    build_windowed_dataset,
    windows_to_sax_patterns,
)
from src.models.automata.automaton import ProbabilisticAutomaton
from src.models.deep_learning.cnn1d import CNN1DModel
from src.models.deep_learning.gru import GRUModel
from src.models.deep_learning.lstm import LSTMModel
from src.data.unseen_generator import (
    create_unseen_scenario,
    extract_sax_vocabulary,
)


class BATADALExperiment:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.dataset_config = config["dataset"]
        self.preprocessing_config = config["preprocessing"]
        self.automata_config = config["automata"]
        self.experiment_config = config["experiment"]

    def run(self) -> None:
        loader = BATADALLoader(
            raw_file=self.dataset_config["raw_file"],
            processed_root=self.dataset_config["processed_root"],
            delimiter=self.dataset_config.get("delimiter", ","),
        )

        processed_path = loader.save_copy("dataset04.csv")
        dataset = pd.read_csv(processed_path)

        if self.dataset_config.get("time_column") in dataset.columns:
            dataset = dataset.sort_values(self.dataset_config["time_column"]).reset_index(drop=True)

        train_df, validation_df, test_df = split_batadal_time(dataset)
        validation_df = self._build_validation_split(train_df)
        train_df = train_df.iloc[: len(train_df) - len(validation_df)]

        pipeline = PreprocessingPipeline(
            scaler_type=self.preprocessing_config["scaler"],
            pca_components=self.preprocessing_config["pca_components"],
        )
        artifacts = pipeline.fit_transform(train_df, validation_df, test_df)

        models = self._build_deep_learning_models()
        self._train_deep_learning_models(models, train_df, validation_df)

        results: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
        for scenario in self.experiment_config["scenarios"]:
            scenario_test_df = self._prepare_scenario_test_df(test_df, train_df, scenario)
            automata_metrics = self._run_automata_scenario(
                artifacts,
                scenario,
                test_df=scenario_test_df,
            )
            deep_metrics = self._evaluate_deep_learning_models(models, scenario_test_df)

            for model_name, metrics in {"automata": automata_metrics, **deep_metrics}.items():
                for key, value in metrics.items():
                    results[scenario][f"{model_name}_{key}"].append(value)

        print("\n=== BATADAL summary ===")
        for scenario, metric_lists in results.items():
            summary = {
                metric: float(mean(values)) if values else 0.0
                for metric, values in metric_lists.items()
            }
            print(f"Scenario: {scenario} → {summary}")

    def _build_deep_learning_models(self) -> dict[str, Any]:
        parameters = {
            "epochs": self.deep_learning_config["epochs"],
            "batch_size": self.deep_learning_config["batch_size"],
            "early_stopping_patience": self.deep_learning_config["early_stopping_patience"],
            "seed": self.experiment_config["seeds"][0],
        }

        models: dict[str, Any] = {}
        for model_name in self.deep_learning_config["enabled_models"]:
            if model_name == "lstm":
                models[model_name] = LSTMModel(**parameters)
            elif model_name == "gru":
                models[model_name] = GRUModel(**parameters)
            elif model_name == "cnn1d":
                models[model_name] = CNN1DModel(**parameters)
            else:
                raise ValueError(f"Unknown deep learning model: {model_name}")
        return models

    def _train_deep_learning_models(
        self,
        models: dict[str, Any],
        train_df: pd.DataFrame,
        validation_df: pd.DataFrame | None,
    ) -> None:
        x_train, y_train = self._prepare_dl_dataset(train_df)
        x_val, y_val = (
            self._prepare_dl_dataset(validation_df)
            if validation_df is not None
            else (None, None)
        )

        if x_train.shape[0] == 0:
            print("⚠️ BATADAL: Yeterli derin öğrenme eğitim verisi yok. Modeller atlanıyor.")
            return

        for model_name, model in models.items():
            print(f"   🧠 Eğitiliyor: {model_name.upper()} ({len(x_train)} örnek)")
            model.fit(x_train, y_train, x_val=x_val, y_val=y_val)

    def _evaluate_deep_learning_models(
        self,
        models: dict[str, Any],
        test_df: pd.DataFrame,
    ) -> dict[str, dict[str, float]]:
        x_test, y_test = self._prepare_dl_dataset(test_df)
        metrics: dict[str, dict[str, float]] = {}

        for model_name, model in models.items():
            if x_test.shape[0] == 0:
                metrics[model_name] = {
                    "accuracy": 0.0,
                    "precision": 0.0,
                    "recall": 0.0,
                    "f1": 0.0,
                }
                continue

            y_pred = model.predict(x_test)
            metrics[model_name] = compute_classification_metrics(y_test, y_pred)

        return metrics

    def _prepare_dl_dataset(
        self,
        df: pd.DataFrame,
    ) -> tuple["np.ndarray", "np.ndarray"]:
        return build_windowed_dataset(
            df["PC1"].tolist(),
            df[self.dataset_config["target_column"]].tolist(),
            self.deep_learning_config["sequence_length"],
        )

    def _prepare_scenario_test_df(
        self,
        test_df: pd.DataFrame,
        train_df: pd.DataFrame,
        scenario: str,
    ) -> pd.DataFrame:
        scenario_df = test_df.copy()
        if scenario == "gaussian_noise":
            return add_gaussian_noise(scenario_df, seed=self.experiment_config["seeds"][0])
        elif scenario == "unseen":
            return create_numeric_unseen_scenario(
                test_df=scenario_df,
                train_df=train_df,
                inject_ratio=0.1,
                seed=self.experiment_config["seeds"][0],
            )
        return scenario_df

    def _build_validation_split(self, train_df: pd.DataFrame) -> pd.DataFrame:
        if len(train_df) < 10:
            return train_df.iloc[:0]

        validation_fraction = self.dataset_config["split"].get("validation_ratio", 0.2)
        validation_size = max(1, int(len(train_df) * validation_fraction))
        return train_df.iloc[-validation_size:]

    def _run_automata_scenario(
        self,
        artifacts: Any,
        scenario: str,
        test_df: pd.DataFrame | None = None,
    ) -> dict[str, float]:
        if test_df is None:
            test_df = artifacts.test.copy()
            if scenario == "gaussian_noise":
                test_df = add_gaussian_noise(test_df, seed=self.experiment_config["seeds"][0])
        else:
            test_df = test_df.copy()

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
