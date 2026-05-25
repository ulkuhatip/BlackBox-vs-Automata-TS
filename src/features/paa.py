from __future__ import annotations

from typing import Sequence


def piecewise_aggregate_approximation(window: Sequence[float], segments: int) -> list[float]:
    """Placeholder PAA implementation."""
    if segments <= 0:
        raise ValueError("segments must be positive")
    return list(window[:segments])
