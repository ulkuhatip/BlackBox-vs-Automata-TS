from __future__ import annotations

from itertools import product
from typing import Sequence

import numpy as np


def extract_sax_vocabulary(patterns: Sequence[str]) -> set[str]:
    """Build a unique SAX vocabulary from training patterns."""
    return set(patterns)


def generate_unseen_patterns(
    vocabulary: set[str],
    alphabet_size: int,
    window_size: int,
    n_unseen: int = 10,
    seed: int | None = None,
) -> list[str]:
    """Generate symbolic patterns that do not exist in the training vocabulary."""
    if alphabet_size <= 0:
        raise ValueError("alphabet_size must be positive")
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if n_unseen <= 0:
        return []

    alphabet = "abcdefghijklmnopqrstuvwxyz"[:alphabet_size]
    rng = np.random.default_rng(seed)
    unseen: list[str] = []
    seen_unseen: set[str] = set()

    base_candidates = [
        candidate
        for candidate in (
            "".join(chars) for chars in product(alphabet, repeat=window_size)
        )
        if candidate not in vocabulary
    ]

    if base_candidates:
        take = min(n_unseen, len(base_candidates))
        if take == len(base_candidates):
            selected = list(base_candidates)
        else:
            selected_indices = rng.choice(len(base_candidates), size=take, replace=False)
            selected = [base_candidates[int(idx)] for idx in selected_indices]

        unseen.extend(selected)
        seen_unseen.update(selected)

    if len(unseen) >= n_unseen:
        return unseen[:n_unseen]

    # If the normal SAX space is exhausted, synthesize extra symbolic patterns
    # with out-of-alphabet symbols so the unseen-handling path can still run.
    fallback_symbols = alphabet[alphabet_size:] + "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    symbol_count = len(fallback_symbols)
    if symbol_count == 0:
        raise RuntimeError("No fallback symbols available for unseen pattern generation")

    start_index = int(rng.integers(0, symbol_count ** min(window_size, 6)))
    candidate_index = start_index

    while len(unseen) < n_unseen:
        value = candidate_index
        chars: list[str] = []
        for _ in range(window_size):
            chars.append(fallback_symbols[value % symbol_count])
            value //= symbol_count
        candidate = "".join(chars)
        if candidate not in vocabulary and candidate not in seen_unseen:
            unseen.append(candidate)
            seen_unseen.add(candidate)
        candidate_index += 1

    return unseen


def create_unseen_scenario(
    series: Sequence[float],
    sax_vocabulary: set[str],
    alphabet_size: int,
    window_size: int,
    inject_ratio: float = 0.1,
    seed: int | None = None,
) -> tuple[list[str], list[bool]]:
    """Inject unseen symbolic patterns into a SAX pattern sequence."""
    from src.features.windowing import windows_to_sax_patterns

    rng = np.random.default_rng(seed)
    patterns = windows_to_sax_patterns(series, window_size, alphabet_size)

    n_inject = max(1, int(len(patterns) * inject_ratio))
    unseen_pool = generate_unseen_patterns(
        vocabulary=sax_vocabulary,
        alphabet_size=alphabet_size,
        window_size=window_size,
        n_unseen=n_inject,
        seed=seed,
    )

    inject_indices = rng.choice(len(patterns), size=n_inject, replace=False)
    is_unseen = [False] * len(patterns)

    for i, idx in enumerate(inject_indices):
        patterns[idx] = unseen_pool[i % len(unseen_pool)]
        is_unseen[idx] = True

    return patterns, is_unseen
