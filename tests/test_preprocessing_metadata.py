import pandas as pd

from src.data.pca import PCAReducer
from src.data.scaling import DatasetScaler


def test_scaler_ignores_string_metadata_columns() -> None:
    df = pd.DataFrame(
        {
            "DATETIME": ["01/08/16 00", "01/08/16 01", "01/08/16 02"],
            "L_T1": [1.0, 2.0, 3.0],
            "L_T2": [2.0, 3.0, 4.0],
            "ATT_FLAG": [0, 1, 0],
        }
    )

    scaler = DatasetScaler()
    scaler.fit(df)
    transformed = scaler.transform(df)

    assert transformed["DATETIME"].tolist() == df["DATETIME"].tolist()
    assert transformed["ATT_FLAG"].tolist() == df["ATT_FLAG"].tolist()


def test_pca_preserves_non_numeric_metadata_columns() -> None:
    df = pd.DataFrame(
        {
            "DATETIME": ["01/08/16 00", "01/08/16 01", "01/08/16 02"],
            "L_T1": [1.0, 2.0, 3.0],
            "L_T2": [2.0, 3.0, 4.0],
            "ATT_FLAG": [0, 1, 0],
        }
    )

    scaler = DatasetScaler().fit(df)
    scaled = scaler.transform(df)
    reducer = PCAReducer(n_components=1).fit(scaled)
    reduced = reducer.transform(scaled)

    assert "PC1" in reduced.columns
    assert reduced["DATETIME"].tolist() == df["DATETIME"].tolist()
    assert reduced["ATT_FLAG"].tolist() == df["ATT_FLAG"].tolist()
