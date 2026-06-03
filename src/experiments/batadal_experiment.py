from __future__ import annotations
from collections import defaultdict
from pathlib import Path
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
from src.explainability.formatter import format_deep_learning_explanation, save_explanations
from src.utils.results import save_results_to_csv
from src.utils.reporting import export_results_to_json, save_comparison_matrices
from src.utils.benchmark import generate_benchmark_report


class BATADALExperiment:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.dataset_config = config["dataset"]
        self.preprocessing_config = config["preprocessing"]
        self.deep_learning_config = config["deep_learning"]
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

        results_root = Path("results/batadal")
        results_root.mkdir(parents=True, exist_ok=True)

        # ========== STAGE 1: Fixed Parameters (Baseline) ==========
        print("\n" + "="*80)
        print("STAGE 1: Fixed Parameters (window_size=4, alphabet_size=3)")
        print("="*80)
        fixed_window = 4
        fixed_alphabet = 3
        stage1_results = self._run_parameter_stage(
            train_df, validation_df, test_df, fixed_window, fixed_alphabet, "Stage1_Fixed"
        )
        self._save_stage_results(stage1_results, results_root, "stage1_fixed")

        # ========== STAGE 2: Parameter Variation (Grid Search) ==========
        print("\n" + "="*80)
        print("STAGE 2: Parameter Grid Search (16 combinations)")
        print("="*80)
        param_grid = self.automata_config.get("param_grid", {})
        window_sizes = param_grid.get("window_size", [4])
        alphabet_sizes = param_grid.get("alphabet_size", [3])

        all_param_results = []
        total_combinations = len(window_sizes) * len(alphabet_sizes)
        current_combo = 0

        for window_size in window_sizes:
            for alphabet_size in alphabet_sizes:
                current_combo += 1
                print(f"\n[{current_combo}/{total_combinations}] Window={window_size}, Alphabet={alphabet_size}")
                print("-" * 60)

                combo_results = self._run_parameter_stage(
                    train_df, validation_df, test_df, window_size, alphabet_size,
                    f"Window{window_size}_Alpha{alphabet_size}"
                )
                all_param_results.append({
                    "window_size": window_size,
                    "alphabet_size": alphabet_size,
                    "results": combo_results,
                })

        # Save individual combination results
        for param_result in all_param_results:
            combo_name = f"stage2_w{param_result['window_size']}_a{param_result['alphabet_size']}"
            self._save_stage_results(param_result["results"], results_root, combo_name)

        # Generate parameter analysis report
        print(f"\n✅ Generating parameter analysis report...")
        self._generate_parameter_analysis_report(all_param_results, results_root)

        print(f"\n✅ BATADAL experiments completed! Results saved to {results_root}/")

    def _run_parameter_stage(
        self,
        train_df: pd.DataFrame,
        validation_df: pd.DataFrame,
        test_df: pd.DataFrame,
        window_size: int,
        alphabet_size: int,
        stage_name: str,
    ) -> dict[str, dict[str, list[float]]]:
        """Run a complete stage with given parameters on time-ordered BATADAL split."""
        pipeline = PreprocessingPipeline(
            scaler_type=self.preprocessing_config["scaler"],
            pca_components=self.preprocessing_config["pca_components"],
        )
        artifacts = pipeline.fit_transform(train_df, validation_df, test_df)

        # Build and train DL models
        models = self._build_deep_learning_models()
        self._train_deep_learning_models(
            models,
            artifacts.train,
            artifacts.validation,
        )

        results: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

        for scenario in self.experiment_config["scenarios"]:
            scenario_test_df = self._prepare_scenario_test_df(test_df, train_df, scenario)
            processed_scenario_test_df = self._transform_scenario_test_df(
                pipeline,
                scenario_test_df,
            )

            # Run automata with current parameters
            automata_metrics = self._run_automata_scenario(
                artifacts,
                scenario,
                test_df=processed_scenario_test_df,
                window_size=window_size,
                alphabet_size=alphabet_size,
            )
            deep_metrics = self._evaluate_deep_learning_models(
                models,
                processed_scenario_test_df,
            )

            for model_name, metrics in {"automata": automata_metrics, **deep_metrics}.items():
                for key, value in metrics.items():
                    results[scenario][f"{model_name}_{key}"].append(value)

        print(f"  ✅ Evaluation completed")
        return results

    def _save_stage_results(
        self,
        results: dict[str, dict[str, list[float]]],
        results_root: Path,
        stage_name: str,
    ) -> None:
        """Save results for a stage."""
        print(f"\n--- {stage_name} Summary ---")
        for scenario, metric_lists in results.items():
            summary = {
                metric: float(mean(values)) if values else 0.0
                for metric, values in metric_lists.items()
            }
            print(f"Scenario: {scenario} → {summary}")

        save_results_to_csv(results, results_root, stage_name)
        export_results_to_json(results, results_root, stage_name)
        save_comparison_matrices(results, results_root, stage_name)
        generate_benchmark_report(results, results_root, stage_name)

    def _generate_parameter_analysis_report(
        self,
        all_param_results: list[dict[str, Any]],
        results_root: Path,
    ) -> None:
        """Generate a comprehensive parameter analysis report."""
        import json
        
        analysis = []
        for param_result in all_param_results:
            window_size = param_result["window_size"]
            alphabet_size = param_result["alphabet_size"]
            results = param_result["results"]

            # Calculate mean metrics across all scenarios
            combo_analysis = {
                "window_size": window_size,
                "alphabet_size": alphabet_size,
                "scenarios": {},
            }

            for scenario, metric_lists in results.items():
                scenario_metrics = {}
                for metric, values in metric_lists.items():
                    if values:
                        scenario_metrics[metric] = {
                            "mean": float(mean(values)),
                            "std": float(pd.Series(values).std()),
                            "min": float(min(values)),
                            "max": float(max(values)),
                        }
                combo_analysis["scenarios"][scenario] = scenario_metrics

            analysis.append(combo_analysis)

        # Save as JSON
        analysis_file = results_root / "parameter_analysis.json"
        with open(analysis_file, "w") as f:
            json.dump(analysis, f, indent=2)

        # Generate markdown report
        report_file = results_root / "parameter_analysis_report.md"
        with open(report_file, "w") as f:
            f.write("# BATADAL Parameter Analysis Report\n\n")
            f.write("## Parameter Grid Search Results\n\n")
            f.write("16 combinations on time-ordered test set\n\n")

            for combo in analysis:
                w_size = combo["window_size"]
                a_size = combo["alphabet_size"]
                f.write(f"### Window Size={w_size}, Alphabet Size={a_size}\n\n")

                for scenario, metrics in combo["scenarios"].items():
                    f.write(f"#### Scenario: {scenario}\n")
                    f.write("| Metric | Mean | Std | Min | Max |\n")
                    f.write("|--------|------|-----|-----|-----|\n")
                    for metric_name, values in metrics.items():
                        f.write(f"| {metric_name} | {values['mean']:.4f} | {values['std']:.4f} | "
                               f"{values['min']:.4f} | {values['max']:.4f} |\n")
                    f.write("\n")

        print(f"✅ Parameter analysis report saved to {report_file}")

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

    def _generate_deep_learning_explanations(
        self,
        models: dict[str, Any],
        test_df: pd.DataFrame,
        scenario: str,
    ) -> None:
        """Generate JSON explanations for deep learning model predictions."""
        x_test, y_test = self._prepare_dl_dataset(test_df)
        
        if x_test.shape[0] == 0:
            return
        
        for model_name, model in models.items():
            predictions = model.predict(x_test)
            proba_dicts = model.predict_proba_dict(x_test)
            
            explanations = []
            for i in range(len(x_test)):
                pred = int(predictions[i])
                prob_dict = proba_dicts[i]
                confidence = prob_dict[pred]
                
                expl = format_deep_learning_explanation(
                    prediction=pred,
                    probability=confidence,
                    probabilities_all_classes=prob_dict,
                    input_shape=x_test[i].shape
                )
                explanations.append(expl)
            
            output_path = Path("outputs/explainability/batadal")
            save_explanations(
                explanations,
                output_path,
                model_name,
                scenario
            )

    def _prepare_scenario_test_df(
        self,
        test_df: pd.DataFrame,
        train_df: pd.DataFrame,
        scenario: str,
    ) -> pd.DataFrame:
        scenario_df = test_df.copy()
        if scenario == "gaussian_noise":
            return add_gaussian_noise(
                scenario_df,
                seed=self.experiment_config["seeds"][0],
                exclude_columns={self.dataset_config["target_column"]},
            )
        elif scenario == "unseen":
            return create_numeric_unseen_scenario(
                test_df=scenario_df,
                train_df=train_df,
                inject_ratio=0.1,
                seed=self.experiment_config["seeds"][0],
            )
        return scenario_df

    def _transform_scenario_test_df(
        self,
        pipeline: PreprocessingPipeline,
        scenario_test_df: pd.DataFrame,
    ) -> pd.DataFrame:
        scaled_df = pipeline.scaler.transform(scenario_test_df)
        return pipeline.pca.transform(scaled_df)

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
        window_size: int | None = None,
        alphabet_size: int | None = None,
    ) -> dict[str, float]:
        # Use provided parameters or fall back to config
        if window_size is None:
            window_size = self.automata_config["window_size"]
        if alphabet_size is None:
            alphabet_size = self.automata_config["alphabet_size"]

        if test_df is None:
            test_df = artifacts.test.copy()
            if scenario == "gaussian_noise":
                test_df = add_gaussian_noise(test_df, seed=self.experiment_config["seeds"][0])
        else:
            test_df = test_df.copy()

        automaton = ProbabilisticAutomaton(
            window_size=window_size,
            alphabet_size=alphabet_size,
            anomaly_threshold=0.15,
        )
        automaton.fit(artifacts.train["PC1"].tolist())

        if scenario == "unseen":
            training_patterns = windows_to_sax_patterns(
                artifacts.train["PC1"].tolist(),
                window_size,
                alphabet_size,
            )
            vocabulary = extract_sax_vocabulary(training_patterns)
            patterns, _ = create_unseen_scenario(
                series=test_df["PC1"].tolist(),
                sax_vocabulary=vocabulary,
                alphabet_size=alphabet_size,
                window_size=window_size,
                seed=self.experiment_config["seeds"][0],
            )
        else:
            patterns = windows_to_sax_patterns(
                test_df["PC1"].tolist(),
                window_size,
                alphabet_size,
            )

        y_true = test_df[self.dataset_config["target_column"]].iloc[window_size - 1 :].to_numpy()
        y_pred = automaton.predict(patterns)
        return compute_classification_metrics(y_true, y_pred)
