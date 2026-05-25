from __future__ import annotations


class DatasetScaler:
    """Placeholder scaler wrapper. Fit only on training data."""

    def fit(self, features):
        return self

    def transform(self, features):
        return features
