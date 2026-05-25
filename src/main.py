from __future__ import annotations

from pathlib import Path

from src.data.batadal_loader import BATADALLoader
from src.data.skab_loader import SKABLoader
from src.utils.config import load_yaml_config


def main() -> None:
    skab_config = load_yaml_config(Path("configs/skab.yaml"))["dataset"]
    batadal_config = load_yaml_config(Path("configs/batadal.yaml"))["dataset"]

    skab_loader = SKABLoader(
        raw_root=skab_config["raw_root"],
        processed_root=skab_config["processed_root"],
        groups=skab_config["groups"],
        delimiter=skab_config["delimiter"],
    )
    batadal_loader = BATADALLoader(
        raw_file=batadal_config["raw_file"],
        processed_root=batadal_config["processed_root"],
        delimiter=batadal_config["delimiter"],
    )

    skab_output = skab_loader.save_combined()
    batadal_output = batadal_loader.save_copy()

    print(f"Combined SKAB dataset saved to: {skab_output}")
    print(f"Prepared BATADAL dataset saved to: {batadal_output}")


if __name__ == "__main__":
    main()
