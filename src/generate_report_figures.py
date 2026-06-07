from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
    auc,
)
from sklearn.model_selection import train_test_split

from src.data.batadal_loader import BATADALLoader
from src.data.preprocess import PreprocessingPipeline
from src.data.skab_loader import SKABLoader
from src.data.splitters import split_batadal_time, split_skab_groups
from src.data.unseen_generator import create_unseen_scenario, extract_sax_vocabulary
from src.features.noise import add_gaussian_noise, create_numeric_unseen_scenario
from src.features.windowing import windows_to_sax_patterns
from src.models.automata.automaton import ProbabilisticAutomaton


ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = ROOT / "results"
OUTPUT_ROOT = ROOT / "outputs" / "figures" / "report"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate report-ready figures for README screenshots.",
    )
    parser.add_argument(
        "--dataset",
        choices=["skab", "batadal", "all"],
        default="all",
        help="Dataset to process.",
    )
    parser.add_argument(
        "--scenario",
        choices=["original", "gaussian_noise", "unseen", "all"],
        default="all",
        help="Scenario to visualize for automata plots.",
    )
    parser.add_argument(
        "--window-size",
        type=int,
        default=6,
        help="Automata window size for rerun figures.",
    )
    parser.add_argument(
        "--alphabet-size",
        type=int,
        default=5,
        help="Automata alphabet size for rerun figures.",
    )
    parser.add_argument(
        "--skab-fold",
        type=int,
        default=1,
        help="Representative SKAB fold to visualize (1-based).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed for scenario generation and split reproducibility.",
    )
    return parser.parse_args()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def clean_axes() -> None:
    plt.tight_layout()
    plt.close()


def save_model_comparison_chart(dataset: str) -> None:
    summary_path = RESULTS_ROOT / dataset / "stage2_w6_a5_results_summary.csv"
    df = pd.read_csv(summary_path)
    output_dir = OUTPUT_ROOT / dataset / "summary"
    ensure_dir(output_dir)

    for metric in ["accuracy", "precision", "recall", "f1"]:
        metric_df = df[df["metric"] == metric].copy()
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=metric_df,
            x="scenario",
            y="mean",
            hue="model",
            palette="Set2",
        )
        plt.ylim(0, 1)
        plt.title(f"{dataset.upper()} Model Comparison ({metric.upper()})")
        plt.ylabel(metric.upper())
        plt.xlabel("Scenario")
        plt.legend(title="Model")
        plt.savefig(output_dir / f"{dataset}_model_comparison_{metric}.png", dpi=180, bbox_inches="tight")
        clean_axes()


def save_parameter_sensitivity_plots(dataset: str) -> None:
    analysis_path = RESULTS_ROOT / dataset / "parameter_analysis.json"
    output_dir = OUTPUT_ROOT / dataset / "parameter_sensitivity"
    ensure_dir(output_dir)

    with analysis_path.open("r", encoding="utf-8") as handle:
        analysis = json.load(handle)

    records: list[dict[str, Any]] = []
    for combo in analysis:
        for scenario, metrics in combo["scenarios"].items():
            for metric_name, values in metrics.items():
                records.append(
                    {
                        "window_size": combo["window_size"],
                        "alphabet_size": combo["alphabet_size"],
                        "scenario": scenario,
                        "metric": metric_name,
                        "mean": values["mean"],
                    }
                )

    df = pd.DataFrame(records)
    automata_df = df[df["metric"].isin(["automata_accuracy", "automata_recall", "automata_f1"])].copy()

    for metric_name in ["automata_accuracy", "automata_recall", "automata_f1"]:
        pretty_name = metric_name.replace("automata_", "").upper()
        for scenario in sorted(automata_df["scenario"].unique()):
            scenario_df = automata_df[
                (automata_df["metric"] == metric_name) & (automata_df["scenario"] == scenario)
            ]
            heatmap_data = scenario_df.pivot(
                index="window_size",
                columns="alphabet_size",
                values="mean",
            ).sort_index()

            plt.figure(figsize=(7, 5))
            sns.heatmap(
                heatmap_data,
                annot=True,
                fmt=".3f",
                cmap="YlGnBu",
                vmin=0,
                vmax=1,
                cbar_kws={"label": pretty_name},
            )
            plt.title(f"{dataset.upper()} Automata {pretty_name} Sensitivity ({scenario})")
            plt.xlabel("Alphabet Size")
            plt.ylabel("Window Size")
            plt.savefig(
                output_dir / f"{dataset}_{scenario}_{metric_name}_heatmap.png",
                dpi=180,
                bbox_inches="tight",
            )
            clean_axes()


def prepare_skab_context(
    config: dict[str, Any],
    fold_index: int,
    seed: int,
) -> dict[str, Any]:
    dataset_cfg = config["dataset"]
    loader = SKABLoader(
        raw_root=dataset_cfg["raw_root"],
        processed_root=dataset_cfg["processed_root"],
        groups=dataset_cfg["groups"],
        delimiter=dataset_cfg.get("delimiter", ";"),
    )
    dataset = loader.load()
    folds = split_skab_groups(
        dataset=dataset,
        group_column=dataset_cfg["split"]["group_column"],
        target_column=dataset_cfg["target_column"],
        n_splits=dataset_cfg["split"]["n_splits"],
    )
    selected_fold = max(1, min(fold_index, len(folds))) - 1
    train_df, test_df = folds[selected_fold]

    if len(train_df) >= 10:
        train_df, validation_df = train_test_split(
            train_df,
            test_size=0.2,
            stratify=train_df[dataset_cfg["target_column"]],
            random_state=seed,
        )
    else:
        validation_df = None

    pipeline = PreprocessingPipeline(
        scaler_type=config["preprocessing"]["scaler"],
        pca_components=config["preprocessing"]["pca_components"],
    )
    artifacts = pipeline.fit_transform(train_df, validation_df, test_df)

    return {
        "dataset_name": "skab",
        "config": config,
        "train_raw": train_df,
        "test_raw": test_df,
        "pipeline": pipeline,
        "artifacts": artifacts,
        "fold_label": f"fold{selected_fold + 1}",
    }


def prepare_batadal_context(
    config: dict[str, Any],
) -> dict[str, Any]:
    dataset_cfg = config["dataset"]
    loader = BATADALLoader(
        raw_file=dataset_cfg["raw_file"],
        processed_root=dataset_cfg["processed_root"],
        delimiter=dataset_cfg.get("delimiter", ","),
    )
    dataset = loader.load()
    time_column = dataset_cfg.get("time_column")
    if time_column in dataset.columns:
        dataset = dataset.sort_values(time_column).reset_index(drop=True)

    train_df, validation_df, test_df = split_batadal_time(dataset)
    validation_size = max(1, int(len(train_df) * dataset_cfg["split"].get("validation_ratio", 0.2)))
    validation_df = train_df.iloc[-validation_size:].copy()
    train_df = train_df.iloc[: len(train_df) - len(validation_df)].copy()

    pipeline = PreprocessingPipeline(
        scaler_type=config["preprocessing"]["scaler"],
        pca_components=config["preprocessing"]["pca_components"],
    )
    artifacts = pipeline.fit_transform(train_df, validation_df, test_df)

    return {
        "dataset_name": "batadal",
        "config": config,
        "train_raw": train_df,
        "test_raw": test_df,
        "pipeline": pipeline,
        "artifacts": artifacts,
        "fold_label": "time_split",
    }


def prepare_scenario_test_df(context: dict[str, Any], scenario: str, seed: int) -> pd.DataFrame:
    config = context["config"]
    dataset_cfg = config["dataset"]
    train_df = context["train_raw"]
    test_df = context["test_raw"].copy()

    if scenario == "gaussian_noise":
        return add_gaussian_noise(
            test_df,
            seed=seed,
            exclude_columns={dataset_cfg["target_column"]},
        )
    if scenario == "unseen":
        return create_numeric_unseen_scenario(
            test_df=test_df,
            train_df=train_df,
            inject_ratio=0.1,
            seed=seed,
        )
    return test_df


def transform_scenario_test_df(context: dict[str, Any], scenario_test_df: pd.DataFrame) -> pd.DataFrame:
    pipeline = context["pipeline"]
    scaled_df = pipeline.scaler.transform(scenario_test_df)
    return pipeline.pca.transform(scaled_df)


def compute_automata_outputs(
    context: dict[str, Any],
    scenario: str,
    window_size: int,
    alphabet_size: int,
    seed: int,
) -> dict[str, Any]:
    config = context["config"]
    dataset_cfg = config["dataset"]
    artifacts = context["artifacts"]

    scenario_test_raw = prepare_scenario_test_df(context, scenario, seed)
    processed_test = transform_scenario_test_df(context, scenario_test_raw)

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
        patterns, unseen_flags = create_unseen_scenario(
            series=processed_test["PC1"].tolist(),
            sax_vocabulary=vocabulary,
            alphabet_size=alphabet_size,
            window_size=window_size,
            seed=seed,
        )
    else:
        patterns = windows_to_sax_patterns(
            processed_test["PC1"].tolist(),
            window_size,
            alphabet_size,
        )
        unseen_flags = [False] * len(patterns)

    y_true = processed_test[dataset_cfg["target_column"]].iloc[window_size - 1 :].to_numpy()
    y_pred = np.asarray(automaton.predict(patterns), dtype=int)
    transition_probs = np.asarray(automaton.predict_proba(patterns), dtype=float)
    anomaly_scores = 1.0 - transition_probs

    return {
        "automaton": automaton,
        "patterns": patterns,
        "unseen_flags": unseen_flags,
        "y_true": y_true,
        "y_pred": y_pred,
        "anomaly_scores": anomaly_scores,
        "transition_probs": transition_probs,
    }


def save_confusion_matrix_plot(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    output_path: Path,
    title: str,
) -> None:
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    plt.figure(figsize=(5, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Normal", "Anomaly"])
    disp.plot(cmap="Blues", colorbar=False)
    plt.title(title)
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    clean_axes()


def save_pr_curve_plot(
    y_true: np.ndarray,
    scores: np.ndarray,
    output_path: Path,
    title: str,
) -> None:
    if len(np.unique(y_true)) < 2:
        return

    precision, recall, _ = precision_recall_curve(y_true, scores)
    pr_auc = auc(recall, precision)
    plt.figure(figsize=(6, 5))
    plt.plot(recall, precision, label=f"PR AUC = {pr_auc:.3f}", color="#1f77b4")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(title)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    clean_axes()


def save_roc_curve_plot(
    y_true: np.ndarray,
    scores: np.ndarray,
    output_path: Path,
    title: str,
) -> None:
    if len(np.unique(y_true)) < 2:
        return

    fpr, tpr, _ = roc_curve(y_true, scores)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f"ROC AUC = {roc_auc:.3f}", color="#d62728")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(title)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    clean_axes()


def save_transition_heatmap(
    automaton: ProbabilisticAutomaton,
    output_path: Path,
    title: str,
    max_states: int = 20,
) -> None:
    state_weights: dict[str, int] = {}
    for (source, target), count in automaton.transition_counts.items():
        state_weights[source] = state_weights.get(source, 0) + count
        state_weights[target] = state_weights.get(target, 0) + count

    states = sorted(
        state_weights,
        key=lambda state: (-state_weights[state], state),
    )[:max_states]

    matrix = pd.DataFrame(0.0, index=states, columns=states)
    for (source, target), prob in automaton.transition_probabilities.items():
        if source in matrix.index and target in matrix.columns:
            matrix.loc[source, target] = prob

    plt.figure(figsize=(max(8, len(states) * 0.5), max(6, len(states) * 0.4)))
    sns.heatmap(
        matrix,
        cmap="mako",
        annot=len(states) <= 12,
        fmt=".2f",
        cbar_kws={"label": "Transition Probability"},
    )
    plt.title(title)
    plt.xlabel("To State")
    plt.ylabel("From State")
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    clean_axes()


def save_state_diagram(
    automaton: ProbabilisticAutomaton,
    output_path: Path,
    title: str,
    max_edges: int = 40,
) -> None:
    graph = nx.DiGraph()
    sorted_edges = sorted(
        automaton.transition_probabilities.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:max_edges]

    for (source, target), prob in sorted_edges:
        graph.add_edge(source, target, weight=prob, label=f"{prob:.2f}")

    if not graph.nodes:
        return

    plt.figure(figsize=(12, 9))
    pos = nx.spring_layout(graph, seed=42, k=1.2)
    edge_widths = [1 + 5 * graph[u][v]["weight"] for u, v in graph.edges()]
    nx.draw_networkx_nodes(graph, pos, node_color="#f4d35e", node_size=1200, edgecolors="black")
    nx.draw_networkx_labels(graph, pos, font_size=9, font_weight="bold")
    nx.draw_networkx_edges(
        graph,
        pos,
        width=edge_widths,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=18,
        edge_color="#4f6d7a",
        connectionstyle="arc3,rad=0.08",
    )
    edge_labels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
    plt.title(title)
    plt.axis("off")
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    clean_axes()


def save_unseen_pattern_plot(
    unseen_flags: list[bool],
    y_true: np.ndarray,
    output_path: Path,
    title: str,
) -> None:
    if not unseen_flags:
        return

    frame = pd.DataFrame(
        {
            "step": np.arange(len(unseen_flags)),
            "unseen": np.asarray(unseen_flags, dtype=int),
            "label": y_true[: len(unseen_flags)],
        }
    )
    plt.figure(figsize=(10, 4))
    plt.plot(frame["step"], frame["label"], label="True label", alpha=0.7)
    plt.scatter(
        frame.loc[frame["unseen"] == 1, "step"],
        frame.loc[frame["unseen"] == 1, "label"],
        color="red",
        label="Injected unseen",
        s=25,
    )
    plt.title(title)
    plt.xlabel("Sequence Step")
    plt.ylabel("Label")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    clean_axes()


def generate_automata_figure_set(
    context: dict[str, Any],
    scenario: str,
    window_size: int,
    alphabet_size: int,
    seed: int,
) -> None:
    dataset = context["dataset_name"]
    fold_label = context["fold_label"]
    output_dir = OUTPUT_ROOT / dataset / scenario
    ensure_dir(output_dir)

    outputs = compute_automata_outputs(
        context=context,
        scenario=scenario,
        window_size=window_size,
        alphabet_size=alphabet_size,
        seed=seed,
    )

    suffix = f"{dataset}_{scenario}_w{window_size}_a{alphabet_size}_{fold_label}"
    title_prefix = f"{dataset.upper()} | {scenario} | w={window_size}, a={alphabet_size}"

    save_confusion_matrix_plot(
        outputs["y_true"],
        outputs["y_pred"],
        output_dir / f"{suffix}_confusion_matrix.png",
        f"{title_prefix} - Confusion Matrix",
    )
    save_pr_curve_plot(
        outputs["y_true"],
        outputs["anomaly_scores"],
        output_dir / f"{suffix}_precision_recall_curve.png",
        f"{title_prefix} - Precision-Recall Curve",
    )
    save_roc_curve_plot(
        outputs["y_true"],
        outputs["anomaly_scores"],
        output_dir / f"{suffix}_roc_curve.png",
        f"{title_prefix} - ROC Curve",
    )
    save_transition_heatmap(
        outputs["automaton"],
        output_dir / f"{suffix}_transition_heatmap.png",
        f"{title_prefix} - Transition Probability Heatmap",
    )
    save_state_diagram(
        outputs["automaton"],
        output_dir / f"{suffix}_state_diagram.png",
        f"{title_prefix} - Automata State Diagram",
    )
    if scenario == "unseen":
        save_unseen_pattern_plot(
            outputs["unseen_flags"],
            outputs["y_true"],
            output_dir / f"{suffix}_unseen_injection_map.png",
            f"{title_prefix} - Unseen Injection Map",
        )


def run_for_dataset(
    dataset: str,
    scenarios: list[str],
    window_size: int,
    alphabet_size: int,
    skab_fold: int,
    seed: int,
) -> None:
    config = load_yaml(ROOT / "configs" / f"{dataset}.yaml")
    save_model_comparison_chart(dataset)
    save_parameter_sensitivity_plots(dataset)

    if dataset == "skab":
        context = prepare_skab_context(config, fold_index=skab_fold, seed=seed)
    else:
        context = prepare_batadal_context(config)

    for scenario in scenarios:
        generate_automata_figure_set(
            context=context,
            scenario=scenario,
            window_size=window_size,
            alphabet_size=alphabet_size,
            seed=seed,
        )


def main() -> None:
    sns.set_theme(style="whitegrid")
    args = parse_args()

    datasets = ["skab", "batadal"] if args.dataset == "all" else [args.dataset]
    scenarios = ["original", "gaussian_noise", "unseen"] if args.scenario == "all" else [args.scenario]

    for dataset in datasets:
        print(f"\nGenerating figures for {dataset.upper()}...")
        run_for_dataset(
            dataset=dataset,
            scenarios=scenarios,
            window_size=args.window_size,
            alphabet_size=args.alphabet_size,
            skab_fold=args.skab_fold,
            seed=args.seed,
        )

    print(f"\nDone. Figures saved under: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
