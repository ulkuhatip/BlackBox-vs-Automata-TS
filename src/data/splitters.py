from __future__ import annotations

import pandas as pd


def split_skab_groups(dataset: pd.DataFrame, group_column: str) -> list[tuple[pd.DataFrame, pd.DataFrame]]:
    """Placeholder for GroupKFold or StratifiedGroupKFold logic."""
    _ = group_column
    return [(dataset.copy(), dataset.iloc[0:0].copy())]


def split_batadal_time(dataset: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split BATADAL in chronological 60/20/20 order."""
    train_end = int(len(dataset) * 0.6)
    validation_end = train_end + int(len(dataset) * 0.2)
    train = dataset.iloc[:train_end].copy()
    validation = dataset.iloc[train_end:validation_end].copy()
    test = dataset.iloc[validation_end:].copy()
    return train, validation, test
