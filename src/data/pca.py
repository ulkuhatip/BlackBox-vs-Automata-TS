from __future__ import annotations
import pandas as pd
from sklearn.decomposition import PCA

class PCAReducer:
    """Compresses multi-dimensional sensor data into Principal Components."""

    def __init__(self, n_components: int = 1) -> None:
        self.pca = PCA(n_components=n_components)
        self.exclude_columns = ['datetime', 'anomaly', 'changepoint', 'source_group', 'source_file', 'ATT_FLAG']

    def _sensor_columns(self, df: pd.DataFrame) -> list[str]:
        return [
            col for col in df.columns
            if col not in self.exclude_columns and pd.api.types.is_numeric_dtype(df[col])
        ]

    def fit(self, df: pd.DataFrame) -> PCAReducer:
        """Fits the PCA reducer ONLY using the scaled training fold."""
        sensor_cols = self._sensor_columns(df)
        self.pca.fit(df[sensor_cols])
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Reduces sensor columns to a single 'PC1' column for the Automata model."""
        df_copy = df.copy()
        sensor_cols = self._sensor_columns(df_copy)
        
        reduced_features = self.pca.transform(df_copy[sensor_cols])
        output_df = pd.DataFrame(reduced_features, columns=["PC1"], index=df_copy.index)
        
        # Merge every non-feature column back to preserve labels and metadata.
        for col in df_copy.columns:
            if col not in sensor_cols:
                output_df[col] = df_copy[col]
                
        return output_df
