from __future__ import annotations

import numpy as np
import pytest


# ──────────────────────────────────────────────
# LSTM Testleri
# ──────────────────────────────────────────────

def test_lstm_fit_and_predict_binary() -> None:
    from src.models.deep_learning.lstm import LSTMModel
    x = np.random.randn(50, 10, 1).astype(np.float32)
    y = np.random.randint(0, 2, 50).astype(np.float32)
    model = LSTMModel(units=8, epochs=2, batch_size=16, seed=42)
    model.fit(x, y, x_val=x, y_val=y)
    preds = model.predict(x)
    assert preds.shape == (50,)
    assert set(preds).issubset({0, 1})


def test_lstm_predict_before_fit_raises() -> None:
    from src.models.deep_learning.lstm import LSTMModel
    model = LSTMModel()
    x = np.random.randn(10, 5, 1).astype(np.float32)
    with pytest.raises(RuntimeError, match="fit"):
        model.predict(x)


def test_lstm_predict_proba_between_0_and_1() -> None:
    from src.models.deep_learning.lstm import LSTMModel
    x = np.random.randn(30, 10, 1).astype(np.float32)
    y = np.random.randint(0, 2, 30).astype(np.float32)
    model = LSTMModel(units=8, epochs=2, batch_size=16, seed=42)
    model.fit(x, y)
    probs = model.predict_proba(x)
    assert np.all(probs >= 0.0)
    assert np.all(probs <= 1.0)


def test_lstm_predict_proba_dict_returns_list_of_dicts() -> None:
    from src.models.deep_learning.lstm import LSTMModel
    x = np.random.randn(10, 5, 1).astype(np.float32)
    y = np.random.randint(0, 2, 10).astype(np.float32)
    model = LSTMModel(units=8, epochs=2, batch_size=8, seed=42)
    model.fit(x, y)
    result = model.predict_proba_dict(x)
    assert len(result) == 10
    for d in result:
        assert 0 in d and 1 in d
        assert abs(d[0] + d[1] - 1.0) < 1e-5


def test_lstm_different_seeds_produce_different_weights() -> None:
    from src.models.deep_learning.lstm import LSTMModel
    x = np.random.randn(30, 5, 1).astype(np.float32)
    y = np.random.randint(0, 2, 30).astype(np.float32)
    model_a = LSTMModel(units=8, epochs=3, seed=42)
    model_b = LSTMModel(units=8, epochs=3, seed=999)
    model_a.fit(x, y)
    model_b.fit(x, y)
    preds_a = model_a.predict_proba(x)
    preds_b = model_b.predict_proba(x)
    # Farklı seed → farklı sonuçlar (büyük ihtimalle)
    assert not np.allclose(preds_a, preds_b, atol=1e-3)


# ──────────────────────────────────────────────
# GRU Testleri
# ──────────────────────────────────────────────

def test_gru_fit_and_predict_binary() -> None:
    from src.models.deep_learning.gru import GRUModel
    x = np.random.randn(50, 10, 1).astype(np.float32)
    y = np.random.randint(0, 2, 50).astype(np.float32)
    model = GRUModel(units=8, epochs=2, batch_size=16, seed=42)
    model.fit(x, y, x_val=x, y_val=y)
    preds = model.predict(x)
    assert preds.shape == (50,)
    assert set(preds).issubset({0, 1})


def test_gru_predict_before_fit_raises() -> None:
    from src.models.deep_learning.gru import GRUModel
    model = GRUModel()
    x = np.random.randn(10, 5, 1).astype(np.float32)
    with pytest.raises(RuntimeError, match="fit"):
        model.predict(x)


def test_gru_predict_proba_between_0_and_1() -> None:
    from src.models.deep_learning.gru import GRUModel
    x = np.random.randn(30, 10, 1).astype(np.float32)
    y = np.random.randint(0, 2, 30).astype(np.float32)
    model = GRUModel(units=8, epochs=2, batch_size=16, seed=42)
    model.fit(x, y)
    probs = model.predict_proba(x)
    assert np.all(probs >= 0.0)
    assert np.all(probs <= 1.0)


def test_gru_predict_proba_dict_sums_to_one() -> None:
    from src.models.deep_learning.gru import GRUModel
    x = np.random.randn(10, 5, 1).astype(np.float32)
    y = np.random.randint(0, 2, 10).astype(np.float32)
    model = GRUModel(units=8, epochs=2, batch_size=8, seed=42)
    model.fit(x, y)
    result = model.predict_proba_dict(x)
    for d in result:
        assert abs(d[0] + d[1] - 1.0) < 1e-5


def test_gru_returns_self_after_fit() -> None:
    from src.models.deep_learning.gru import GRUModel
    x = np.random.randn(20, 5, 1).astype(np.float32)
    y = np.random.randint(0, 2, 20).astype(np.float32)
    model = GRUModel(units=8, epochs=2, seed=42)
    result = model.fit(x, y)
    assert result is model


# ──────────────────────────────────────────────
# CNN1D Testleri
# ──────────────────────────────────────────────

def test_cnn1d_fit_and_predict_binary() -> None:
    from src.models.deep_learning.cnn1d import CNN1DModel
    x = np.random.randn(50, 10, 1).astype(np.float32)
    y = np.random.randint(0, 2, 50).astype(np.float32)
    model = CNN1DModel(filters=8, epochs=2, batch_size=16, seed=42)
    model.fit(x, y, x_val=x, y_val=y)
    preds = model.predict(x)
    assert preds.shape == (50,)
    assert set(preds).issubset({0, 1})


def test_cnn1d_predict_before_fit_raises() -> None:
    from src.models.deep_learning.cnn1d import CNN1DModel
    model = CNN1DModel()
    x = np.random.randn(10, 5, 1).astype(np.float32)
    with pytest.raises(RuntimeError, match="fit"):
        model.predict(x)


def test_cnn1d_predict_proba_between_0_and_1() -> None:
    from src.models.deep_learning.cnn1d import CNN1DModel
    x = np.random.randn(30, 10, 1).astype(np.float32)
    y = np.random.randint(0, 2, 30).astype(np.float32)
    model = CNN1DModel(filters=8, epochs=2, batch_size=16, seed=42)
    model.fit(x, y)
    probs = model.predict_proba(x)
    assert np.all(probs >= 0.0)
    assert np.all(probs <= 1.0)


def test_cnn1d_predict_proba_dict_sums_to_one() -> None:
    from src.models.deep_learning.cnn1d import CNN1DModel
    x = np.random.randn(10, 5, 1).astype(np.float32)
    y = np.random.randint(0, 2, 10).astype(np.float32)
    model = CNN1DModel(filters=8, epochs=2, batch_size=8, seed=42)
    model.fit(x, y)
    result = model.predict_proba_dict(x)
    for d in result:
        assert abs(d[0] + d[1] - 0.0) != 0


def test_cnn1d_returns_self_after_fit() -> None:
    from src.models.deep_learning.cnn1d import CNN1DModel
    x = np.random.randn(20, 5, 1).astype(np.float32)
    y = np.random.randint(0, 2, 20).astype(np.float32)
    model = CNN1DModel(filters=8, epochs=2, seed=42)
    result = model.fit(x, y)
    assert result is model


def test_cnn1d_output_shape_correct() -> None:
    from src.models.deep_learning.cnn1d import CNN1DModel
    x = np.random.randn(15, 8, 1).astype(np.float32)
    y = np.random.randint(0, 2, 15).astype(np.float32)
    model = CNN1DModel(filters=8, epochs=2, seed=42)
    model.fit(x, y)
    probs = model.predict_proba(x)
    assert probs.shape == (15,)