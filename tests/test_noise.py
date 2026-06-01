import numpy as np
import pandas as pd

from src.features.noise import add_gaussian_noise


def test_add_gaussian_noise_changes_numeric_columns_only() -> None:
    df = pd.DataFrame(
        {
            "datetime": ["2024-01-01", "2024-01-02"],
            "sensor_a": [1.0, 2.0],
            "sensor_b": [3.0, 4.0],
            "label": [0, 1],
        }
    )

    result = add_gaussian_noise(
        df,
        std=0.1,
        seed=123,
        exclude_columns={"label"},
    )

    assert list(result["datetime"]) == ["2024-01-01", "2024-01-02"]
    assert list(result["label"]) == [0, 1]
    assert not np.array_equal(result[["sensor_a", "sensor_b"]].values, df[["sensor_a", "sensor_b"]].values)
    assert result["sensor_a"].dtype == float
    assert result["sensor_b"].dtype == float


def test_add_gaussian_noise_with_zero_std_returns_same_numeric_data() -> None:
    df = pd.DataFrame(
        {
            "sensor_a": [1.0, 2.0],
            "sensor_b": [3.0, 4.0],
        }
    )

    result = add_gaussian_noise(df, std=0.0, seed=42)

    assert result.equals(df)
