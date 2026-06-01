from __future__ import annotations
from collections import defaultdict
from typing import Any, Sequence

from src.explainability.decision_formatter import format_decision_payload
from src.explainability.probabilistic_explainer import path_probability
from src.features.windowing import windows_to_sax_patterns
from src.models.automata.transitions import build_transition_probabilities
from src.models.automata.unseen_handler import map_unseen_pattern


class ProbabilisticAutomaton:
    """Probabilistic automaton built from SAX transition frequencies."""

    def __init__(
        self,
        window_size: int = 4,
        alphabet_size: int = 3,
        anomaly_threshold: float = 0.15,
        default_transition_probability: float | None = None,
    ) -> None:
        self.window_size = window_size
        self.alphabet_size = alphabet_size
        self.anomaly_threshold = anomaly_threshold
        self.default_transition_probability = default_transition_probability
        self.vocabulary: set[str] = set()
        self.transition_counts: dict[tuple[str, str], int] = {}
        self.transition_probabilities: dict[tuple[str, str], float] = {}
        self.train_patterns: list[str] = []

    def fit(self, series: Sequence[float]) -> "ProbabilisticAutomaton":
        self.train_patterns = windows_to_sax_patterns(
            series,
            self.window_size,
            self.alphabet_size,
        )
        if len(self.train_patterns) < 2:
            raise ValueError("At least two SAX patterns are required to build an automaton.")

        self.vocabulary = set(self.train_patterns)
        self.transition_counts = self._count_transitions(self.train_patterns)
        self.transition_probabilities = build_transition_probabilities(self.transition_counts)

        if self.default_transition_probability is None:
            self.default_transition_probability = 1.0 / max(1, len(self.vocabulary))

        return self

    def _count_transitions(self, patterns: Sequence[str]) -> dict[tuple[str, str], int]:
        counts: dict[tuple[str, str], int] = defaultdict(int)
        for source, target in zip(patterns, patterns[1:]):
            counts[(source, target)] += 1
        return dict(counts)

    def _resolve_pattern(self, pattern: str) -> tuple[str, bool, int]:
        if pattern in self.vocabulary:
            return pattern, False, 0
        mapped, distance = map_unseen_pattern(pattern, self.vocabulary)
        return mapped, True, distance

    def _transition_probability(self, source: str, target: str) -> float:
        return self.transition_probabilities.get((source, target), self.default_transition_probability)

    def explain(self, patterns: Sequence[str]) -> dict[str, Any]:
        if not self.transition_probabilities:
            raise RuntimeError("Automaton must be fitted before calling explain().")

        steps: list[dict[str, Any]] = []
        resolved_patterns: list[str] = []

        for idx, pattern in enumerate(patterns):
            resolved, unseen, distance = self._resolve_pattern(pattern)
            resolved_patterns.append(resolved)
            if idx == 0:
                steps.append(
                    {
                        "time_step": idx + self.window_size,
                        "state": resolved,
                        "pattern": pattern,
                        "status": "seen" if not unseen else "unseen",
                        "mapped_to": resolved if unseen else None,
                        "distance": distance,
                        "transition_probability": 1.0,
                        "anomaly": 0,
                    }
                )
                continue

            previous_state = resolved_patterns[idx - 1]
            prob = self._transition_probability(previous_state, resolved)
            anomaly_flag = 1 if prob < self.anomaly_threshold else 0
            steps.append(
                {
                    "time_step": idx + self.window_size,
                    "state": previous_state,
                    "pattern": pattern,
                    "status": "unseen" if unseen else "seen",
                    "mapped_to": resolved if unseen else None,
                    "distance": distance,
                    "transition_probability": prob,
                    "anomaly": anomaly_flag,
                }
            )

        transition_probs = [step["transition_probability"] for step in steps[1:]]
        path_prob = path_probability(transition_probs) if transition_probs else 1.0
        decision = "anomaly" if any(step["anomaly"] for step in steps[1:]) else "normal"
        confidence_score = float(path_prob)

        payload = {
            "sequence_length": len(patterns),
            "path_probability": confidence_score,
            "decision": decision,
            "confidence_score": confidence_score,
            "steps": steps,
        }
        return format_decision_payload(payload)

    def predict(self, patterns: Sequence[str]) -> list[int]:
        explanation = self.explain(patterns)
        return [int(step["anomaly"]) for step in explanation["steps"]]

    def predict_proba(self, patterns: Sequence[str]) -> list[float]:
        explanation = self.explain(patterns)
        return [float(step["transition_probability"]) for step in explanation["steps"]]
