from __future__ import annotations
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class DatasetScaler:
    """Scales sensor features while keeping metadata columns intact."""

    def __init__(self, scaler_type: str = "standard") -> None:
        if scaler_type == "standard":
            self.scaler = StandardScaler()
        elif scaler_type == "minmax":
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaler type: {scaler_type}")
            
        self.exclude_columns = ['datetime', 'anomaly', 'changepoint', 'source_group', 'source_file', 'ATT_FLAG']

    def fit(self, df: pd.DataFrame) -> DatasetScaler:
        """Learns the mean and variance ONLY from the training fold."""
        sensor_cols = [col for col in df.columns if col not in self.exclude_columns]
        self.scaler.fit(df[sensor_cols])
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies the learned scaling parameters to any given subset."""
        df_copy = df.copy()
        sensor_cols = [col for col in df_copy.columns if col not in self.exclude_columns]
        df_copy[sensor_cols] = self.scaler.transform(df_copy[sensor_cols])
        return df_copy