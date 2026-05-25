from __future__ import annotations

from typing import Sequence


def sliding_windows(sequence: Sequence[float], window_size: int) -> list[Sequence[float]]:
    """Return overlapping sliding windows over a sequence."""
    return [sequence[index : index + window_size] for index in range(0, len(sequence) - window_size + 1)]
