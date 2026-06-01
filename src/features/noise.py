from __future__ import annotations

import numpy as np
import pandas as pd


def add_gaussian_noise(
    dataset: pd.DataFrame,
    std: float = 0.01,
    seed: int | None = None,
    numeric_only: bool = True,
    exclude_columns: set[str] | None = None,
) -> pd.DataFrame:
    """
    Veri setine Gaussian (Normal) gürültü ekler.

    Parametreler
    ----------
    dataset         : Girdi DataFrame
    std             : Gürültünün standart sapması (varsayılan: 0.01)
    seed            : Tekrarlanabilirlik için random seed
    numeric_only    : True ise yalnızca sayısal sütunlara gürültü ekler
    exclude_columns : Gürültü eklenmeyecek sütun kümeleri

    Döndürür
    --------
    Gürültü eklenmiş yeni bir DataFrame (orijinal bozulmaz)
    """
    if std < 0:
        raise ValueError("std must be non-negative")

    rng = np.random.default_rng(seed)
    result = dataset.copy()

    if exclude_columns is None:
        exclude_columns = {
            "datetime",
            "anomaly",
            "changepoint",
            "source_group",
            "source_file",
            "ATT_FLAG",
            "PC1",
        }

    if numeric_only:
        numeric_cols = [
            col
            for col in result.select_dtypes(include=[np.number]).columns
            if col not in exclude_columns
        ]
    else:
        numeric_cols = [col for col in result.columns if col not in exclude_columns]

    if not numeric_cols:
        return result

    noise = rng.normal(loc=0.0, scale=std, size=(len(result), len(numeric_cols)))
    result[numeric_cols] = result[numeric_cols].values + noise

    return result


def create_numeric_unseen_scenario(
    test_df: pd.DataFrame,
    train_df: pd.DataFrame,
    inject_ratio: float = 0.1,
    seed: int | None = None,
) -> pd.DataFrame:
    """
    Test aşamasında sayısal açıdan unseen (eğitimde görülmeyen) pattern'lar enjekte eder.
    
    Yöntem:
    - Eğitim verisinin değer aralığı (min/max) belirlenir
    - Test verisinin belirli konumlarında bu aralığın dışında değerler üretilir
    - Bu değerler "daha önce gözlenmeyen" anomalous pattern'ları temsil eder
    - Automata'daki SAX-based unseen ile paralel: eğitim sözlüğü dışındaki pattern'lar
    
    Parametreler
    ----------
    test_df      : Test DataFrame (sensör sütunları + etiketler)
    train_df     : Eğitim DataFrame (aralık belirleme için)
    inject_ratio : Kaç oranında satırın unseen değerlerle değiştirilmesi (0.0-1.0, varsayılan 0.1)
    seed         : Random seed (tekrarlanabilirlik)
    
    Döndürür
    --------
    Unseen pattern'lar enjekte edilmiş DataFrame
    """
    rng = np.random.default_rng(seed)
    result = test_df.copy()
    
    # Numerik sütunları belirle (metadata hariç)
    exclude_columns = {'datetime', 'anomaly', 'changepoint', 'source_group', 'source_file', 'ATT_FLAG', 'PC1'}
    numeric_cols = result.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col not in exclude_columns]
    
    if not numeric_cols or len(train_df) == 0:
        return result
    
    # Eğitim aralıklarını belirle
    train_ranges = {}
    for col in numeric_cols:
        if col in train_df.columns:
            col_data = train_df[col]
            train_min = col_data.min()
            train_max = col_data.max()
            train_std = col_data.std()
            if pd.isna(train_std) or train_std <= 0:
                train_std = 1.0
            train_ranges[col] = {
                'min': train_min,
                'max': train_max,
                'std': train_std,
            }
    
    # Hangi satırlara unseen enjekte edeceğini seç
    n_inject = max(1, int(len(result) * inject_ratio))
    inject_indices = rng.choice(len(result), size=n_inject, replace=False)
    
    # Unseen değerler enjekte et (eğitim aralığının dışında)
    for col in numeric_cols:
        if col not in train_ranges:
            continue
        
        train_min = train_ranges[col]['min']
        train_max = train_ranges[col]['max']
        train_std = train_ranges[col]['std']
        
        # Eğitim aralığının dışında rastgele değerler üret
        # Eğitim verisinde +2 STD'den daha yüksek anomali enjekte et
        unseen_values = rng.normal(
            loc=train_max + 2 * train_std,
            scale=train_std,
            size=len(inject_indices)
        )
        
        for i, idx in enumerate(inject_indices):
            result.loc[idx, col] = unseen_values[i]
    
    return result