from __future__ import annotations


def path_probability(transitions: list[float]) -> float:
    """Multiply transition probabilities along a path."""
    probability = 1.0
    for value in transitions:
        probability *= value
    return probability
