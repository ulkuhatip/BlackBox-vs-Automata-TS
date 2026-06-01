from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np


def format_automata_explanation(
    pattern: str,
    mapped_pattern: str,
    distance: int,
    transition_prob: float,
    decision: int,
    confidence: float,
) -> dict[str, Any]:
    """
    Format automata model decision explanation in JSON.
    
    Output structure:
    {
        "decision": 1,
        "confidence": 0.85,
        "pattern_analysis": {
            "observed_pattern": "abc",
            "mapped_pattern": "abc",
            "levenshtein_distance": 0
        },
        "transition_probability": 0.15,
        "interpretation": "..."
    }
    """
    if mapped_pattern == pattern:
        interpretation = f"Pattern '{pattern}' recognized in vocabulary (exact match)"
    else:
        interpretation = (
            f"Pattern '{pattern}' not in vocabulary. "
            f"Mapped to '{mapped_pattern}' (Levenshtein distance: {distance})"
        )

    return {
        "decision": int(decision),
        "confidence": float(confidence),
        "pattern_analysis": {
            "observed_pattern": pattern,
            "mapped_pattern": mapped_pattern,
            "levenshtein_distance": distance,
        },
        "transition_probability": float(transition_prob),
        "interpretation": interpretation,
    }


def format_deep_learning_explanation(
    prediction: int,
    probability: float,
    probabilities_all_classes: dict[int, float],
    input_shape: tuple[int, ...],
) -> dict[str, Any]:
    """
    Format deep learning model decision explanation in JSON.
    
    Output structure:
    {
        "decision": 1,
        "confidence": 0.92,
        "probabilities": {
            "0": 0.08,
            "1": 0.92
        },
        "input_shape": [32, 1],
        "interpretation": "..."
    }
    """
    confidence_pct = probability * 100
    interpretation = (
        f"Model predicts class {prediction} with {confidence_pct:.1f}% confidence. "
        f"Class probabilities: {', '.join(f'{k}={v:.3f}' for k, v in probabilities_all_classes.items())}"
    )

    return {
        "decision": int(prediction),
        "confidence": float(probability),
        "probabilities": {str(k): float(v) for k, v in probabilities_all_classes.items()},
        "input_shape": list(input_shape),
        "interpretation": interpretation,
    }


def save_explanations(
    explanations: list[dict[str, Any]],
    output_path: Path,
    model_name: str,
    scenario: str,
) -> None:
    """Save explanations to JSON file with metadata."""
    output_path.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "metadata": {
            "model": model_name,
            "scenario": scenario,
            "total_predictions": len(explanations),
        },
        "explanations": explanations,
    }
    
    file_path = output_path / f"{model_name}_{scenario}_explanations.json"
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
