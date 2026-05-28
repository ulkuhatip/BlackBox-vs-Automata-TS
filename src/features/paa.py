from __future__ import annotations

import numpy as np
from typing import Sequence


def piecewise_aggregate_approximation(series: Sequence[float], segments: int) -> list[float]:
    """
    Piecewise Aggregate Approximation (PAA).

    Zaman serisini `segments` adet eşit parçaya böler ve
    her parçanın ortalamasını alır. Boyutu düşürür, gürültüyü azaltır.
    """
    if segments <= 0:
        raise ValueError("segments must be positive")

    series = list(series)
    n = len(series)

    if segments > n:
        raise ValueError(f"segments ({segments}) cannot exceed series length ({n})")

    arr = np.array(series, dtype=float)
    # Her segmentin kaç orijinal nokta içerdiğini hesapla (float bölme)
    result = []
    for i in range(segments):
        start = int(np.floor(i * n / segments))
        end = int(np.floor((i + 1) * n / segments))
        end = max(end, start + 1)  # En az 1 nokta
        result.append(float(np.mean(arr[start:end])))

    return result