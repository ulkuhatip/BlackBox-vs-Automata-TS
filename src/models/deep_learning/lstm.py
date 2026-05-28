from __future__ import annotations

import numpy as np
import tensorflow as tf
from tensorflow import keras


class LSTMModel:
    """
    LSTM tabanlı zaman serisi anomali tespiti modeli.

    Proje kuralları:
    - Epoch üst sınırı: 50
    - Batch size: 32
    - Early stopping: validation loss, patience=5
    - Random seed: dışarıdan verilir (42, 123, 2026, 7, 999)
    """

    def __init__(
        self,
        units: int = 64,
        dropout: float = 0.2,
        learning_rate: float = 1e-3,
        epochs: int = 50,
        batch_size: int = 32,
        early_stopping_patience: int = 5,
        seed: int = 42,
    ) -> None:
        self.units = units
        self.dropout = dropout
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.early_stopping_patience = early_stopping_patience
        self.seed = seed
        self.model_: keras.Model | None = None

    def _set_seed(self) -> None:
        tf.random.set_seed(self.seed)
        np.random.seed(self.seed)

    def _build(self, input_shape: tuple[int, int]) -> keras.Model:
        self._set_seed()
        model = keras.Sequential(
            [
                keras.layers.Input(shape=input_shape),
                keras.layers.LSTM(self.units, return_sequences=False),
                keras.layers.Dropout(self.dropout),
                keras.layers.Dense(32, activation="relu"),
                keras.layers.Dense(1, activation="sigmoid"),
            ]
        )
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss="binary_crossentropy",
            metrics=["accuracy"],
        )
        return model

    def fit(
        self,
        x_train: np.ndarray,
        y_train: np.ndarray,
        x_val: np.ndarray | None = None,
        y_val: np.ndarray | None = None,
    ) -> "LSTMModel":
        """
        Modeli eğitir.

        x_train shape: (n_samples, timesteps, features)
        y_train shape: (n_samples,)
        """
        input_shape = (x_train.shape[1], x_train.shape[2])
        self.model_ = self._build(input_shape)

        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor="val_loss",
                patience=self.early_stopping_patience,
                restore_best_weights=True,
            )
        ]

        validation_data = (x_val, y_val) if x_val is not None else None

        self.model_.fit(
            x_train,
            y_train,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_data=validation_data,
            callbacks=callbacks,
            verbose=0,
        )
        return self

    def predict(self, x_test: np.ndarray) -> np.ndarray:
        """
        Tahmin üretir. 0.5 eşiği ile binary çıktı döner.
        """
        if self.model_ is None:
            raise RuntimeError("Model henüz eğitilmedi. Önce fit() çağırın.")
        probs = self.model_.predict(x_test, verbose=0).flatten()
        return (probs >= 0.5).astype(int)

    def predict_proba(self, x_test: np.ndarray) -> np.ndarray:
        """Ham olasılık skorlarını döner."""
        if self.model_ is None:
            raise RuntimeError("Model henüz eğitilmedi. Önce fit() çağırın.")
        return self.model_.predict(x_test, verbose=0).flatten()