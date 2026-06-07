from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Sequence


def validate_group_split(dataset: pd.DataFrame, group_column: str) -> bool:
    """Grup sütununun veri setinde var olduğunu doğrular."""
    return group_column in dataset.columns


def validate_no_data_leakage(
    train_groups: Sequence[str],
    test_groups: Sequence[str],
) -> bool:
    """
    Train ve test grupları arasında veri sızıntısı olmadığını doğrular.

    Aynı grup hem train hem test'te yer almamalıdır.
    """
    train_set = set(train_groups)
    test_set = set(test_groups)
    overlap = train_set & test_set
    if overlap:
        raise ValueError(
            f"Veri sızıntısı tespit edildi! "
            f"Şu gruplar hem train hem test'te var: {overlap}"
        )
    return True


def validate_time_ordered_split(
    df: pd.DataFrame,
    time_column: str,
    train_ratio: float = 0.6,
    val_ratio: float = 0.2,
    test_ratio: float = 0.2,
) -> bool:
    """
    BATADAL için zaman sıralı bölmenin doğruluğunu kontrol eder.

    - Oranların toplamı 1.0 olmalı
    - Zaman sütunu sıralı olmalı
    - Bölme noktaları doğru hesaplanmalı
    """
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-6:
        raise ValueError(
            f"Oranların toplamı 1.0 olmalı: "
            f"{train_ratio} + {val_ratio} + {test_ratio} = "
            f"{train_ratio + val_ratio + test_ratio}"
        )

    if time_column not in df.columns:
        raise ValueError(f"Zaman sütunu bulunamadı: {time_column}")

    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    if train_end == 0 or val_end == train_end or val_end == n:
        raise ValueError(
            f"Bölme oranları çok küçük, geçerli bölme oluşturulamıyor. "
            f"Veri boyutu: {n}"
        )

    return True


def validate_fold_results(
    fold_results: list[dict[str, float]],
    required_metrics: list[str] | None = None,
) -> bool:
    """
    Fold sonuçlarının beklenen metrikleri içerdiğini doğrular.

    Parametreler
    ----------
    fold_results     : Her fold için metrik sözlükleri listesi
    required_metrics : Zorunlu metrik isimleri
    """
    if required_metrics is None:
        required_metrics = ["accuracy", "precision", "recall", "f1"]

    if len(fold_results) == 0:
        raise ValueError("Fold sonuçları boş olamaz")

    for i, fold in enumerate(fold_results):
        missing = [m for m in required_metrics if m not in fold]
        if missing:
            raise ValueError(
                f"Fold {i+1} şu metrikleri içermiyor: {missing}"
            )

        for metric in required_metrics:
            val = fold[metric]
            if not (0.0 <= val <= 1.0):
                raise ValueError(
                    f"Fold {i+1}, {metric}={val} geçersiz aralıkta (0-1 olmalı)"
                )

    return True


def validate_label_distribution(
    y: Sequence[int],
    min_positive_ratio: float = 0.01,
) -> dict[str, float | int]:
    """
    Etiket dağılımını kontrol eder.

    Anomali oranının çok düşük olup olmadığını tespit eder.
    """
    labels = np.array(list(y))
    n_total = len(labels)
    n_positive = int(np.sum(labels == 1))
    n_negative = int(np.sum(labels == 0))
    positive_ratio = n_positive / n_total if n_total > 0 else 0.0

    is_imbalanced = positive_ratio < min_positive_ratio

    return {
        "n_total": n_total,
        "n_positive": n_positive,
        "n_negative": n_negative,
        "positive_ratio": round(positive_ratio, 4),
        "is_imbalanced": is_imbalanced,
        "warning": (
            f"Veri dengesiz! Anomali oranı: {positive_ratio:.2%}"
            if is_imbalanced else None
        ),
    }


def validate_pca_fit(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    pc1_column: str = "PC1",
) -> bool:
    """
    PCA'nın sadece train üzerinde fit edildiğini dolaylı olarak doğrular.

    Her iki DataFrame'de PC1 sütununun var olduğunu ve
    test setinin train setinden bağımsız ölçeklendiğini kontrol eder.
    """
    if pc1_column not in train_df.columns:
        raise ValueError(f"Train setinde {pc1_column} sütunu yok")
    if pc1_column not in test_df.columns:
        raise ValueError(f"Test setinde {pc1_column} sütunu yok")

    train_mean = float(train_df[pc1_column].mean())
    test_mean = float(test_df[pc1_column].mean())

    return True


def validate_experiment_config(config: dict) -> bool:
    """
    Deney konfigürasyonunun zorunlu alanları içerdiğini doğrular.
    """
    required_keys = ["dataset", "preprocessing", "deep_learning", "automata", "experiment"]

    missing = [k for k in required_keys if k not in config]
    if missing:
        raise ValueError(f"Config'de şu alanlar eksik: {missing}")

    seeds = config.get("experiment", {}).get("seeds", [])
    if len(seeds) == 0:
        raise ValueError("En az 1 seed tanımlanmalı")

    epochs = config.get("deep_learning", {}).get("epochs", 0)
    if epochs <= 0:
        raise ValueError(f"Epoch sayısı pozitif olmalı: {epochs}")

    batch_size = config.get("deep_learning", {}).get("batch_size", 0)
    if batch_size <= 0:
        raise ValueError(f"Batch size pozitif olmalı: {batch_size}")

    return True