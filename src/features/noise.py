from __future__ import annotations

import numpy as np
import pandas as pd


def add_gaussian_noise(
    dataset: pd.DataFrame,
    std: float = 0.01,
    seed: int | None = None,
    numeric_only: bool = True,
) -> pd.DataFrame:
    """
    Veri setine Gaussian (Normal) gürültü ekler.

    Parametreler
    ----------
    dataset     : Girdi DataFrame
    std         : Gürültünün standart sapması (varsayılan: 0.01)
    seed        : Tekrarlanabilirlik için random seed
    numeric_only: True ise yalnızca sayısal sütunlara gürültü ekler

    Döndürür
    --------
    Gürültü eklenmiş yeni bir DataFrame (orijinal bozulmaz)
    """
    if std < 0:
        raise ValueError("std must be non-negative")

    rng = np.random.default_rng(seed)
    result = dataset.copy()

    if numeric_only:
        numeric_cols = result.select_dtypes(include=[np.number]).columns
    else:
        numeric_cols = result.columns

    noise = rng.normal(loc=0.0, scale=std, size=(len(result), len(numeric_cols)))
    result[numeric_cols] = result[numeric_cols].values + noise

    return result