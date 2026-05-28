from __future__ import annotations

import numpy as np
from typing import Sequence

# Gaussian dağılım breakpoint'leri (scipy olmadan, önceden hesaplanmış)
# alphabet_size -> breakpoint listesi (len = alphabet_size - 1)
_BREAKPOINTS: dict[int, list[float]] = {
    2: [0.0],
    3: [-0.4307, 0.4307],
    4: [-0.6745, 0.0, 0.6745],
    5: [-0.8416, -0.2533, 0.2533, 0.8416],
    6: [-0.9674, -0.4307, 0.0, 0.4307, 0.9674],
    7: [-1.0675, -0.5659, -0.1800, 0.1800, 0.5659, 1.0675],
    8: [-1.1503, -0.6745, -0.3186, 0.0, 0.3186, 0.6745, 1.1503],
}

_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def sax_transform(values: Sequence[float], alphabet_size: int) -> str:
    """
    SAX (Symbolic Aggregate approXimation) dönüşümü.

    Normalleştirilmiş sayısal değerleri harflere çevirir.
    Gaussian breakpoint'lerine göre hangi bölgeye düştüğünü bulur.
    
    Örnek: alphabet_size=3 → breakpoints=[-0.43, 0.43]
      değer < -0.43  → 'a'
      -0.43 ≤ değer < 0.43 → 'b'
      değer ≥ 0.43  → 'c'
    """
    if alphabet_size < 2:
        raise ValueError("alphabet_size must be at least 2")
    if alphabet_size > len(_ALPHABET):
        raise ValueError(f"alphabet_size cannot exceed {len(_ALPHABET)}")

    breakpoints = _BREAKPOINTS.get(alphabet_size)
    if breakpoints is None:
        raise ValueError(f"No breakpoints defined for alphabet_size={alphabet_size}. Use 2-8.")

    result = []
    for val in values:
        # Hangi bölgeye düştüğünü bul (np.searchsorted ile)
        idx = int(np.searchsorted(breakpoints, val, side="left"))
        result.append(_ALPHABET[idx])

    return "".join(result)