from __future__ import annotations
from pathlib import Path
import pandas as pd

from src.data.batadal_loader import BATADALLoader
from src.data.skab_loader import SKABLoader
from src.data.splitters import split_skab_groups, split_batadal_time
from src.utils.config import load_yaml_config

def main() -> None:
    print("🚀 STARTING MACHINE LEARNING PIPELINE CRADLE 🚀\n")
    
    # Load configuration parameters
    skab_config = load_yaml_config(Path("configs/skab.yaml"))["dataset"]
    batadal_config = load_yaml_config(Path("configs/batadal.yaml"))["dataset"]

    # Initialize data loaders (using your exact architecture)
    skab_loader = SKABLoader(
        raw_root=skab_config["raw_root"],
        processed_root=skab_config["processed_root"],
        groups=skab_config["groups"],
        delimiter=skab_config.get("delimiter", ";"),
    )
    batadal_loader = BATADALLoader(
        raw_file=batadal_config["raw_file"],
        processed_root=batadal_config["processed_root"],
        delimiter=batadal_config["delimiter"],
    )

    # Persist data using your exact method name
    skab_output = skab_loader.save_combined("combined.csv")
    batadal_output = batadal_loader.save_copy("dataset04.csv")
    print(f"📁 Raw data processed and saved to: {skab_output}")
    print(f"📁 Raw data processed and saved to: {batadal_output}\n")

    print("--- Testing Dataset Splitter Modules ---")
    
    # Test SKAB cross-validation group splitting logic (handles your disk format safely)
    skab_df = pd.read_csv(skab_output)
    skab_folds = split_skab_groups(
        dataset=skab_df, 
        group_column=skab_config["split"]["group_column"],
        target_column=skab_config["target_column"],
        n_splits=skab_config["split"]["n_splits"]
    )
    
    # Test BATADAL chronological time splitting logic
    batadal_df = pd.read_csv(batadal_output)
    b_train, b_val, b_test = split_batadal_time(batadal_df)
    print(f"✂️ BATADAL: Train={len(b_train)} | Val={len(b_val)} | Test={len(b_test)}")
    
    print("\n🎉 ARCHITECTURE TEST COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()