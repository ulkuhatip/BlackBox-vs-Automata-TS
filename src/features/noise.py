from __future__ import annotations

import pandas as pd


def add_gaussian_noise(dataset: pd.DataFrame, std: float = 0.01) -> pd.DataFrame:
    """Return a copy of the dataset. Noise injection will be added later."""
    _ = std
    return dataset.copy()
