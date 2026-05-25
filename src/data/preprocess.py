from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class PreprocessArtifacts:
    train: pd.DataFrame
    validation: pd.DataFrame | None
    test: pd.DataFrame


class PreprocessingPipeline:
    """Placeholder preprocessing pipeline for scaling and PCA steps."""

    def fit_transform(
        self,
        train_df: pd.DataFrame,
        validation_df: pd.DataFrame | None,
        test_df: pd.DataFrame,
    ) -> PreprocessArtifacts:
        return PreprocessArtifacts(
            train=train_df.copy(),
            validation=None if validation_df is None else validation_df.copy(),
            test=test_df.copy(),
        )
