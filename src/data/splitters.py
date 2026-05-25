from __future__ import annotations
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

def split_skab_groups(
    dataset: pd.DataFrame, 
    group_column: str = "source_file",
    target_column: str = "anomaly",
    n_splits: int = 5
) -> list[tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Splits the SKAB dataset into 5 folds using StratifiedGroupKFold.
    Fixes duplicate filenames by combining source_group and source_file in memory.
    """
    print(f"✂️ Splitter: Initializing StratifiedGroupKFold with {n_splits} splits...")
    
    # Dynamic fix: Create a temporary unique identifier in memory without touching the disk file
    temp_dataset = dataset.copy()
    temp_dataset["unique_group_id"] = temp_dataset["source_group"] + "_" + temp_dataset[group_column]
    
    sgkf = StratifiedGroupKFold(n_splits=n_splits)
    
    X = temp_dataset.drop(columns=[target_column])
    y = temp_dataset[target_column]
    groups = temp_dataset["unique_group_id"] # Use the fixed dynamic ID for perfect grouping
    
    folds_artifacts = []
    
    for fold_idx, (train_idx, test_idx) in enumerate(sgkf.split(X, y, groups)):
        train_fold = dataset.iloc[train_idx].copy()
        test_fold = dataset.iloc[test_idx].copy()
        
        folds_artifacts.append((train_fold, test_fold))
        print(f"   Fold {fold_idx + 1}: Train rows = {len(train_fold)} | Test rows = {len(test_fold)}")
        
    print("✅ Splitter: Group-based cross-validation splits are ready.")
    return folds_artifacts

def split_batadal_time(dataset: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Splits BATADAL dataset in chronological 60/20/20 order to prevent data leakage."""
    train_end = int(len(dataset) * 0.6)
    validation_end = train_end + int(len(dataset) * 0.2)
    
    train = dataset.iloc[:train_end].copy()
    validation = dataset.iloc[train_end:validation_end].copy()
    test = dataset.iloc[validation_end:].copy()
    
    return train, validation, test