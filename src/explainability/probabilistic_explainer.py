from __future__ import annotations

import math
from typing import Any, Sequence


def path_probability(transitions: Sequence[float]) -> float:
    """
    Ardışık geçiş olasılıklarının çarpımını hesaplar.

    Proje dokümanı Formül C:
    P(sequence) = ∏ P(Si → Si+1)

    Düşük olasılık → anomali adayı
    """
    if not transitions:
        return 0.0

    probability = 1.0
    for value in transitions:
        if value <= 0.0:
            return 0.0
        probability *= value
    return probability


def log_path_probability(transitions: Sequence[float]) -> float:
    """
    Sayısal kararlılık için log olasılık hesaplar.

    Çok uzun dizilerde çarpım sıfıra yaklaşabilir,
    log toplamı daha kararlıdır.
    """
    if not transitions:
        return float("-inf")

    log_prob = 0.0
    for value in transitions:
        if value <= 0.0:
            return float("-inf")
        log_prob += math.log(value)
    return log_prob


def classify_probability(
    probability: float,
    anomaly_threshold: float = 0.15,
) -> dict[str, Any]:
    """
    Olasılık değerini anomali/normal kararına dönüştürür.

    Proje dokümanı yorumu:
    - Düşük olasılık → Anomali olasılığı yüksek
    - Yüksek olasılık → Normal davranış
    """
    if probability <= 0.0:
        confidence_level = "Very Low"
        decision = "anomaly"
    elif probability < anomaly_threshold:
        confidence_level = "Low"
        decision = "anomaly"
    elif probability < 0.5:
        confidence_level = "Medium"
        decision = "normal"
    else:
        confidence_level = "High"
        decision = "normal"

    return {
        "decision": decision,
        "probability": probability,
        "confidence_level": confidence_level,
        "is_anomaly": decision == "anomaly",
    }


def explain_decision(
    time_step: int,
    previous_state: str,
    incoming_pattern: str,
    vocabulary: set[str],
    transition_probs: dict[tuple[str, str], float],
    nearest_pattern: str | None = None,
    edit_distance: int | None = None,
    anomaly_threshold: float = 0.15,
) -> dict[str, Any]:
    """
    Proje dokümanındaki örnek açıklama formatını üretir.

    [SYSTEM DECISION]
    Time Step: t = 5
    Previous State: "aab"
    Incoming Pattern: "adc"
    Status: Unseen
    Nearest Pattern: "abc" (distance = 1)
    Transitions: aab -> abc : 0.72
    Path Probability: ...
    Decision: ANOMALY
    Confidence Score: 0.108 (Low)
    """
    is_unseen = incoming_pattern not in vocabulary
    effective_pattern = nearest_pattern if (is_unseen and nearest_pattern) else incoming_pattern

    # Geçiş olasılıklarını topla
    transitions = []
    transition_details = {}

    current = previous_state
    if effective_pattern:
        key = (current, effective_pattern)
        prob = transition_probs.get(key, 0.0)
        transitions.append(prob)
        transition_details[f"{current} -> {effective_pattern}"] = prob

    prob = path_probability(transitions)
    classification = classify_probability(prob, anomaly_threshold)

    explanation = {
        "time_step": time_step,
        "previous_state": previous_state,
        "incoming_pattern": incoming_pattern,
        "status": "unseen" if is_unseen else "seen",
        "nearest_pattern": nearest_pattern if is_unseen else None,
        "edit_distance": edit_distance if is_unseen else None,
        "transitions": transition_details,
        "path_probability": prob,
        "decision": classification["decision"],
        "confidence_score": prob,
        "confidence_level": classification["confidence_level"],
        "is_anomaly": classification["is_anomaly"],
    }

    return explanation


def explain_sequence(
    patterns: Sequence[str],
    vocabulary: set[str],
    transition_probs: dict[tuple[str, str], float],
    unseen_mappings: dict[str, tuple[str, int]] | None = None,
    anomaly_threshold: float = 0.15,
    start_time_step: int = 0,
) -> list[dict[str, Any]]:
    """
    Bir pattern dizisi için tüm kararları açıklar.

    Her adım için:
    - Seen/unseen durumu
    - Geçiş olasılıkları
    - Path probability
    - Anomali kararı
    """
    if unseen_mappings is None:
        unseen_mappings = {}

    explanations = []
    patterns = list(patterns)

    for i in range(1, len(patterns)):
        previous = patterns[i - 1]
        current = patterns[i]

        nearest = None
        distance = None
        if current not in vocabulary and current in unseen_mappings:
            nearest, distance = unseen_mappings[current]

        explanation = explain_decision(
            time_step=start_time_step + i,
            previous_state=previous,
            incoming_pattern=current,
            vocabulary=vocabulary,
            transition_probs=transition_probs,
            nearest_pattern=nearest,
            edit_distance=distance,
            anomaly_threshold=anomaly_threshold,
        )
        explanations.append(explanation)

    return explanations


def format_explanation_text(explanation: dict[str, Any]) -> str:
    """
    Proje dokümanındaki metin formatında açıklama üretir.

    [SYSTEM DECISION]
    Time Step: t = 5
    ...
    """
    lines = [
        "[SYSTEM DECISION]",
        f"Time Step: t = {explanation['time_step']}",
        f"Previous State: \"{explanation['previous_state']}\"",
        f"Incoming Pattern: \"{explanation['incoming_pattern']}\"",
        f"Status: {'Unseen' if explanation['status'] == 'unseen' else 'Seen'}",
    ]

    if explanation.get("nearest_pattern"):
        lines.append(
            f"Nearest Pattern: \"{explanation['nearest_pattern']}\" "
            f"(distance = {explanation['edit_distance']})"
        )

    if explanation.get("transitions"):
        lines.append("Transitions:")
        for transition, prob in explanation["transitions"].items():
            lines.append(f"  {transition} : {prob:.2f}")

    prob = explanation["path_probability"]
    lines.append(f"Path Probability: {prob:.4f}")
    lines.append(
        f"Decision: {'ANOMALY' if explanation['is_anomaly'] else 'NORMAL'}"
    )
    lines.append(
        f"Confidence Score: {prob:.4f} ({explanation['confidence_level']})"
    )

    return "\n".join(lines)


def compute_sequence_statistics(
    explanations: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Bir dizi açıklama üzerinden istatistikler üretir.

    - Toplam anomali sayısı
    - Unseen pattern oranı
    - Ortalama path probability
    """
    if not explanations:
        return {
            "n_steps": 0,
            "n_anomalies": 0,
            "n_unseen": 0,
            "anomaly_rate": 0.0,
            "unseen_rate": 0.0,
            "mean_probability": 0.0,
        }

    n_steps = len(explanations)
    n_anomalies = sum(1 for e in explanations if e["is_anomaly"])
    n_unseen = sum(1 for e in explanations if e["status"] == "unseen")
    probs = [e["path_probability"] for e in explanations]

    return {
        "n_steps": n_steps,
        "n_anomalies": n_anomalies,
        "n_unseen": n_unseen,
        "anomaly_rate": n_anomalies / n_steps,
        "unseen_rate": n_unseen / n_steps,
        "mean_probability": float(sum(probs) / len(probs)),
        "min_probability": float(min(probs)),
        "max_probability": float(max(probs)),
    }