from __future__ import annotations

import pandas as pd


def validate_group_split(dataset: pd.DataFrame, group_column: str) -> bool:
    """Basic validation that the requested group column exists."""
    return group_column in dataset.columns
