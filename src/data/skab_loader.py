from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data.loaders import DatasetPaths


class SKABLoader:
    """Load and combine SKAB valve1 and valve2 CSV files into one dataset."""

    def __init__(
        self,
        raw_root: str | Path,
        processed_root: str | Path,
        groups: list[str],
        delimiter: str = ";",
    ) -> None:
        self.paths = DatasetPaths(
            raw_root=Path(raw_root),
            processed_root=Path(processed_root),
        )
        self.groups = groups
        self.delimiter = delimiter

    def load(self) -> pd.DataFrame:
        frames: list[pd.DataFrame] = []

        for group_name in self.groups:
            group_dir = self.paths.raw_root / group_name
            csv_files = sorted(group_dir.glob("*.csv"), key=lambda path: int(path.stem))

            if not csv_files:
                raise FileNotFoundError(f"No CSV files found in {group_dir}")

            for csv_path in csv_files:
                frame = pd.read_csv(csv_path, sep=self.delimiter)
                frame["source_group"] = group_name
                frame["source_file"] = csv_path.name
                frames.append(frame)

        if not frames:
            raise ValueError("No SKAB records were loaded.")

        return pd.concat(frames, ignore_index=True)

    def save_combined(self, filename: str = "combined.csv") -> Path:
        dataset = self.load()
        self.paths.processed_root.mkdir(parents=True, exist_ok=True)
        output_path = self.paths.processed_root / filename
        dataset.to_csv(output_path, index=False)
        return output_path
