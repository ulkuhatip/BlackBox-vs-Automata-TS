from __future__ import annotations

import numpy as np
from scipy import stats
from scipy.stats import wilcoxon, chi2_contingency
from typing import Sequence


def wilcoxon_test(
    scores_a: Sequence[float],
    scores_b: Sequence[float],
    alternative: str = "two-sided",
) -> dict[str, float | str]:
    """
    Wilcoxon işaretli sıralama testi.

    İki modelin F1 skorları arasındaki farkın istatistiksel
    olarak anlamlı olup olmadığını test eder.

    Parametreler
    ----------
    scores_a : Model A'nın fold bazlı skorları
    scores_b : Model B'nin fold bazlı skorları
    alternative : 'two-sided', 'greater', 'less'

    Döndürür
    --------
    test istatistiği, p değeri ve yorum
    """
    a = np.array(list(scores_a), dtype=float)
    b = np.array(list(scores_b), dtype=float)

    if len(a) != len(b):
        raise ValueError(f"Skorlar eşit uzunlukta olmalı: {len(a)} != {len(b)}")

    if len(a) < 2:
        return {
            "test": "wilcoxon",
            "statistic": float("nan"),
            "p_value": 1.0,
            "significant": False,
            "interpretation": "Yetersiz veri (en az 2 fold gerekli)",
        }

    # Tüm farklar sıfırsa test yapılamaz
    differences = a - b
    if np.all(differences == 0):
        return {
            "test": "wilcoxon",
            "statistic": 0.0,
            "p_value": 1.0,
            "significant": False,
            "interpretation": "Modeller arasında fark yok",
        }

    try:
        stat, p_value = wilcoxon(a, b, alternative=alternative)
        significant = bool(p_value < 0.05)
        return {
            "test": "wilcoxon",
            "statistic": float(stat),
            "p_value": float(p_value),
            "significant": significant,
            "interpretation": (
                f"p={p_value:.4f} → {'Anlamlı fark var (p<0.05)' if significant else 'Anlamlı fark yok (p≥0.05)'}"
            ),
        }
    except Exception as exc:
        return {
            "test": "wilcoxon",
            "statistic": float("nan"),
            "p_value": 1.0,
            "significant": False,
            "interpretation": f"Test yapılamadı: {exc}",
        }


def mcnemar_test(
    y_true: Sequence[int],
    y_pred_a: Sequence[int],
    y_pred_b: Sequence[int],
) -> dict[str, float | str]:
    """
    McNemar testi.

    İki sınıflandırıcının hata örüntülerinin farklı olup
    olmadığını test eder. Contingency tablosu üzerinden çalışır.

    Parametreler
    ----------
    y_true   : Gerçek etiketler
    y_pred_a : Model A tahminleri
    y_pred_b : Model B tahminleri

    Döndürür
    --------
    test istatistiği, p değeri ve yorum
    """
    y_true = list(y_true)
    y_pred_a = list(y_pred_a)
    y_pred_b = list(y_pred_b)

    if not (len(y_true) == len(y_pred_a) == len(y_pred_b)):
        raise ValueError("Tüm diziler eşit uzunlukta olmalı")

    # Contingency tablosu: [A doğru B yanlış, A yanlış B doğru]
    # n01: A yanlış, B doğru
    # n10: A doğru, B yanlış
    n01 = sum(
        1 for t, a, b in zip(y_true, y_pred_a, y_pred_b)
        if a != t and b == t
    )
    n10 = sum(
        1 for t, a, b in zip(y_true, y_pred_a, y_pred_b)
        if a == t and b != t
    )

    if n01 + n10 == 0:
        return {
            "test": "mcnemar",
            "n01": 0,
            "n10": 0,
            "statistic": 0.0,
            "p_value": 1.0,
            "significant": False,
            "interpretation": "Her iki model de aynı örneklerde hata yapıyor",
        }

    # McNemar istatistiği (süreklilik düzeltmesi ile)
    statistic = (abs(n01 - n10) - 1) ** 2 / (n01 + n10)
    p_value = float(1 - stats.chi2.cdf(statistic, df=1))
    significant = bool(p_value < 0.05)

    return {
        "test": "mcnemar",
        "n01": n01,
        "n10": n10,
        "statistic": float(statistic),
        "p_value": p_value,
        "significant": significant,
        "interpretation": (
            f"n01={n01}, n10={n10}, p={p_value:.4f} → "
            f"{'Modeller istatistiksel olarak farklı (p<0.05)' if significant else 'Modeller istatistiksel olarak benzer (p≥0.05)'}"
        ),
    }


def compare_models(
    results_a: Sequence[float],
    results_b: Sequence[float],
    model_a_name: str = "Model A",
    model_b_name: str = "Model B",
) -> dict[str, float | str]:
    """
    İki modeli Wilcoxon testi ile karşılaştırır.

    Fold bazlı F1 skorlarını alır, istatistiksel anlamlılığı test eder.
    """
    a = np.array(list(results_a), dtype=float)
    b = np.array(list(results_b), dtype=float)

    wilcoxon_result = wilcoxon_test(a, b)

    return {
        "model_a": model_a_name,
        "model_b": model_b_name,
        "mean_a": float(np.mean(a)),
        "mean_b": float(np.mean(b)),
        "std_a": float(np.std(a)),
        "std_b": float(np.std(b)),
        "mean_diff": float(np.mean(a) - np.mean(b)),
        **wilcoxon_result,
    }


def summarize_fold_results(
    fold_scores: Sequence[float],
    model_name: str = "model",
    metric_name: str = "f1",
) -> dict[str, float | str]:
    """
    Fold bazlı sonuçları özetler.

    Ortalama, standart sapma, min, max değerlerini hesaplar.
    Rapor formatı: mean ± std
    """
    scores = np.array(list(fold_scores), dtype=float)

    if len(scores) == 0:
        return {
            "model": model_name,
            "metric": metric_name,
            "mean": 0.0,
            "std": 0.0,
            "min": 0.0,
            "max": 0.0,
            "summary": "0.000 ± 0.000",
            "n_folds": 0,
        }

    mean = float(np.mean(scores))
    std = float(np.std(scores))
    return {
        "model": model_name,
        "metric": metric_name,
        "mean": mean,
        "std": std,
        "min": float(np.min(scores)),
        "max": float(np.max(scores)),
        "summary": f"{mean:.3f} ± {std:.3f}",
        "n_folds": len(scores),
    }


def compare_all_models(
    results: dict[str, list[float]],
    baseline_model: str | None = None,
) -> list[dict[str, float | str]]:
    """
    Tüm modelleri birbirleriyle karşılaştırır.

    Parametreler
    ----------
    results       : {model_adı: [fold_f1_skorları]} sözlüğü
    baseline_model: Karşılaştırma için referans model adı

    Döndürür
    --------
    Tüm çift karşılaştırmalarının listesi
    """
    model_names = list(results.keys())
    comparisons = []

    if baseline_model and baseline_model in results:
        # Baseline ile karşılaştır
        for name in model_names:
            if name == baseline_model:
                continue
            comparison = compare_models(
                results[baseline_model],
                results[name],
                model_a_name=baseline_model,
                model_b_name=name,
            )
            comparisons.append(comparison)
    else:
        # Tüm çiftleri karşılaştır
        for i in range(len(model_names)):
            for j in range(i + 1, len(model_names)):
                comparison = compare_models(
                    results[model_names[i]],
                    results[model_names[j]],
                    model_a_name=model_names[i],
                    model_b_name=model_names[j],
                )
                comparisons.append(comparison)

    return comparisons