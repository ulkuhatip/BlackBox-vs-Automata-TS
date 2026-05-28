from __future__ import annotations

from typing import Sequence


def sliding_windows(sequence: Sequence[float], window_size: int) -> list[list[float]]:
    """
    Sliding window (Kayan Pencere) ile alt diziler üret.

    Örnek: sequence=[1,2,3,4,5], window_size=3
      → [[1,2,3], [2,3,4], [3,4,5]]
    """
    if window_size <= 0:
        raise ValueError("window_size must be positive")

    seq = list(sequence)
    n = len(seq)

    if window_size > n:
        return []

    return [seq[i: i + window_size] for i in range(n - window_size + 1)]


def windows_to_sax_patterns(
    sequence: Sequence[float],
    window_size: int,
    alphabet_size: int,
    paa_segments: int | None = None,
) -> list[str]:
    """
    Zaman serisinden SAX pattern listesi üret.

    Her pencereye PAA uygular, sonra SAX ile harfe çevirir.
    paa_segments belirtilmezse window_size kadar segment kullanılır.
    """
    from src.features.paa import piecewise_aggregate_approximation
    from src.features.sax import sax_transform

    if paa_segments is None:
        paa_segments = window_size

    windows = sliding_windows(sequence, window_size)
    patterns = []
    for window in windows:
        paa_repr = piecewise_aggregate_approximation(window, paa_segments)
        symbol = sax_transform(paa_repr, alphabet_size)
        patterns.append(symbol)

    return patterns