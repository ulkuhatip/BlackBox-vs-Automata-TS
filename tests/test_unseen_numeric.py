import numpy as np
import pandas as pd

from src.features.noise import create_numeric_unseen_scenario


def test_create_numeric_unseen_scenario_injects_out_of_range_values() -> None:
    train_df = pd.DataFrame(
        {
            "sensor_a": [0.0, 0.1, 0.2, 0.3, 0.4],
            "sensor_b": [1.0, 1.1, 1.2, 1.3, 1.4],
            "ATT_FLAG": [0, 0, 0, 0, 0],
        }
    )
    test_df = pd.DataFrame(
        {
            "sensor_a": [0.05, 0.15, 0.25, 0.35, 0.45],
            "sensor_b": [1.05, 1.15, 1.25, 1.35, 1.45],
            "ATT_FLAG": [0, 0, 0, 0, 0],
        }
    )

    result = create_numeric_unseen_scenario(test_df=test_df, train_df=train_df, inject_ratio=0.4, seed=42)

    # verify injection count and unseen range
    injected = (result["sensor_a"] > train_df["sensor_a"].max()) | (result["sensor_a"] < train_df["sensor_a"].min())
    assert injected.sum() >= 1
    assert all(result.loc[injected, "sensor_a"] > train_df["sensor_a"].max())
    assert all(result.loc[injected, "sensor_b"] > train_df["sensor_b"].max())
    assert result.shape == test_df.shape


def test_create_numeric_unseen_scenario_handles_empty_train() -> None:
    train_df = pd.DataFrame(
        {
            "sensor_a": [],
            "sensor_b": [],
            "ATT_FLAG": [],
        }
    )
    test_df = pd.DataFrame(
        {
            "sensor_a": [0.1, 0.2],
            "sensor_b": [1.1, 1.2],
            "ATT_FLAG": [0, 1],
        }
    )

    result = create_numeric_unseen_scenario(test_df=test_df, train_df=train_df, inject_ratio=0.5, seed=7)

    assert result.equals(test_df)
