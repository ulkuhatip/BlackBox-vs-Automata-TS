from pathlib import Path

import pandas as pd

from src.data.batadal_loader import BATADALLoader


def test_batadal_loader_class_exists() -> None:
    assert BATADALLoader is not None


def test_batadal_loader_normalizes_att_flag_to_binary(tmp_path: Path) -> None:
    raw_file = tmp_path / "batadal.csv"
    pd.DataFrame(
        {
            "DATETIME": ["01/08/16 00", "01/08/16 01", "01/08/16 02"],
            "L_T1": [1.0, 2.0, 3.0],
            "ATT_FLAG": [-999, 1, -999],
        }
    ).to_csv(raw_file, index=False)

    loader = BATADALLoader(
        raw_file=raw_file,
        processed_root=tmp_path / "processed",
    )

    dataset = loader.load()

    assert dataset["ATT_FLAG"].tolist() == [0, 1, 0]
