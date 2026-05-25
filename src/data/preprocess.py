from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

from src.data.scaling import DatasetScaler
from src.data.pca import PCAReducer

@dataclass
class PreprocessArtifacts:
    """Container for holding fully processed splits ready for the models."""
    train: pd.DataFrame
    validation: pd.DataFrame | None
    test: pd.DataFrame

class PreprocessingPipeline:
    """Manages the execution flow of scaling and PCA for each cross-validation loop."""

    def __init__(self, scaler_type: str = "standard", pca_components: int = 1) -> None:
        self.scaler = DatasetScaler(scaler_type=scaler_type)
        self.pca = PCAReducer(n_components=pca_components)

    def fit_transform(
        self,
        train_df: pd.DataFrame,
        validation_df: pd.DataFrame | None,
        test_df: pd.DataFrame,
    ) -> PreprocessArtifacts:
        
        # Step 1: Fit and transform scaling on the current loop data
        self.scaler.fit(train_df)
        scaled_train = self.scaler.transform(train_df)
        scaled_test = self.scaler.transform(test_df)
        scaled_val = self.scaler.transform(validation_df) if validation_df is not None else None
        
        print("⚙️ Pipeline: Executing PCA dimensionality reduction...")
        
        # Step 2: Fit and transform PCA on the scaled data
        self.pca.fit(scaled_train)
        final_train = self.pca.transform(scaled_train)
        final_test = self.pca.transform(scaled_test)
        final_val = self.pca.transform(scaled_val) if scaled_val is not None else None
        
        print("✅ Pipeline: Scaling and PCA compression successfully finished.")
        
        return PreprocessArtifacts(
            train=final_train,
            validation=final_val,
            test=final_test,
        )