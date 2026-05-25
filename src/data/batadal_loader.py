from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data.loaders import DatasetPaths


class BATADALLoader:
    """Load the BATADAL training dataset used in the project."""

    def __init__(
        self,
        raw_file: str | Path,
        processed_root: str | Path,
        delimiter: str = ",",
    ) -> None:
        raw_path = Path(raw_file)
        self.raw_file = raw_path
        self.paths = DatasetPaths(
            raw_root=raw_path.parent,
            processed_root=Path(processed_root),
        )
        self.delimiter = delimiter

    def load(self) -> pd.DataFrame:
        return pd.read_csv(self.raw_file, sep=self.delimiter, skipinitialspace=True)

    def save_copy(self, filename: str = "dataset04.csv") -> Path:
        dataset = self.load()
        self.paths.processed_root.mkdir(parents=True, exist_ok=True)
        output_path = self.paths.processed_root / filename
        dataset.to_csv(output_path, index=False)
        return output_path
