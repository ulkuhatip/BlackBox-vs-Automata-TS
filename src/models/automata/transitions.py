from __future__ import annotations


def build_transition_probabilities(transitions: dict[tuple[str, str], int]) -> dict[tuple[str, str], float]:
    """Convert transition counts to probabilities."""
    totals: dict[str, int] = {}
    for (source, _target), count in transitions.items():
        totals[source] = totals.get(source, 0) + count

    probabilities: dict[tuple[str, str], float] = {}
    for edge, count in transitions.items():
        probabilities[edge] = count / totals[edge[0]]
    return probabilities
