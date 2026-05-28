from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Sequence


def extract_sax_vocabulary(patterns: Sequence[str]) -> set[str]:
    """
    Eğitim verisi pattern listesinden SAX sözlüğü oluşturur.
    
    Parametreler
    ----------
    patterns : Eğitim verisindeki SAX pattern listesi
    
    Döndürür
    --------
    Benzersiz pattern'lardan oluşan sözlük (set)
    """
    return set(patterns)


def generate_unseen_patterns(
    vocabulary: set[str],
    alphabet_size: int,
    window_size: int,
    n_unseen: int = 10,
    seed: int | None = None,
) -> list[str]:
    """
    Sözlükte BULUNMAYAN rastgele SAX pattern'ları üretir.
    
    Proje gereksinimi: Test sırasında sözlükte bulunmayan pattern'lar
    unseen olarak kabul edilir.
    
    Parametreler
    ----------
    vocabulary    : Eğitim verisinden çıkarılan SAX sözlüğü
    alphabet_size : SAX alfabe boyutu (ör. 3 → a,b,c)
    window_size   : Pattern uzunluğu
    n_unseen      : Üretilecek unseen pattern sayısı
    seed          : Tekrarlanabilirlik için random seed
    
    Döndürür
    --------
    Sözlükte bulunmayan pattern listesi
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"[:alphabet_size]
    rng = np.random.default_rng(seed)

    unseen = []
    max_attempts = n_unseen * 1000

    for _ in range(max_attempts):
        if len(unseen) >= n_unseen:
            break
        candidate = "".join(rng.choice(list(alphabet), size=window_size))
        if candidate not in vocabulary:
            unseen.append(candidate)

    if len(unseen) < n_unseen:
        raise RuntimeError(
            f"Yalnızca {len(unseen)} unseen pattern üretilebildi "
            f"(istenen: {n_unseen}). alphabet_size veya window_size artırın."
        )

    return unseen


def create_unseen_scenario(
    series: Sequence[float],
    sax_vocabulary: set[str],
    alphabet_size: int,
    window_size: int,
    inject_ratio: float = 0.1,
    seed: int | None = None,
) -> tuple[list[str], list[bool]]:
    """
    Orijinal SAX pattern dizisine unseen pattern'lar enjekte eder.
    
    Test senaryosu için: bazı konumlara sözlük dışı pattern ekler.
    
    Parametreler
    ----------
    series        : Orijinal PC1 zaman serisi
    sax_vocabulary: Eğitim sözlüğü
    alphabet_size : SAX alfabe boyutu
    window_size   : Pencere boyutu
    inject_ratio  : Kaç oranında pattern'ın unseen olacağı (0.0-1.0)
    seed          : Random seed
    
    Döndürür
    --------
    (pattern_listesi, is_unseen_listesi) tuple'ı
    """
    from src.features.windowing import windows_to_sax_patterns

    rng = np.random.default_rng(seed)

    # Orijinal pattern'ları üret
    patterns = windows_to_sax_patterns(series, window_size, alphabet_size)

    # Unseen pattern havuzu oluştur
    n_inject = max(1, int(len(patterns) * inject_ratio))
    unseen_pool = generate_unseen_patterns(
        vocabulary=sax_vocabulary,
        alphabet_size=alphabet_size,
        window_size=window_size,
        n_unseen=n_inject,
        seed=seed,
    )

    # Hangi indekslere unseen enjekte edileceğini seç
    inject_indices = rng.choice(len(patterns), size=n_inject, replace=False)
    is_unseen = [False] * len(patterns)

    for i, idx in enumerate(inject_indices):
        patterns[idx] = unseen_pool[i % len(unseen_pool)]
        is_unseen[idx] = True

    return patterns, is_unseen