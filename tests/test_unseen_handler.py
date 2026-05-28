from __future__ import annotations

import pytest

from src.models.automata.unseen_handler import levenshtein_distance, map_unseen_pattern
from src.data.unseen_generator import (
    extract_sax_vocabulary,
    generate_unseen_patterns,
    create_unseen_scenario,
)


# ──────────────────────────────────────────────
# Levenshtein Distance Testleri
# ──────────────────────────────────────────────

def test_levenshtein_distance_exact_match() -> None:
    """Aynı string → mesafe 0 olmalı."""
    assert levenshtein_distance("abc", "abc") == 0


def test_levenshtein_distance_empty_strings() -> None:
    """İki boş string → mesafe 0."""
    assert levenshtein_distance("", "") == 0


def test_levenshtein_distance_one_empty() -> None:
    """Bir string boşsa → diğerinin uzunluğu kadar."""
    assert levenshtein_distance("", "abc") == 3
    assert levenshtein_distance("abc", "") == 3


def test_levenshtein_distance_single_substitution() -> None:
    """Tek karakter değişimi → mesafe 1."""
    assert levenshtein_distance("abc", "adc") == 1


def test_levenshtein_distance_single_insertion() -> None:
    """Tek ekleme → mesafe 1."""
    assert levenshtein_distance("ab", "abc") == 1


def test_levenshtein_distance_single_deletion() -> None:
    """Tek silme → mesafe 1."""
    assert levenshtein_distance("abc", "ab") == 1


def test_levenshtein_distance_completely_different() -> None:
    """Tamamen farklı → maksimum mesafe."""
    assert levenshtein_distance("aaa", "bbb") == 3


def test_levenshtein_distance_symmetric() -> None:
    """Mesafe simetrik olmalı: d(x,y) == d(y,x)."""
    assert levenshtein_distance("abc", "bca") == levenshtein_distance("bca", "abc")


# ──────────────────────────────────────────────
# Map Unseen Pattern Testleri
# ──────────────────────────────────────────────

def test_map_unseen_pattern_returns_closest_pattern() -> None:
    """Proje dokümanındaki örnek: 'adc' → 'abc' (mesafe=1)."""
    mapped, distance = map_unseen_pattern("adc", {"abc", "bcc"})
    assert mapped == "abc"
    assert distance == 1


def test_map_unseen_pattern_exact_in_vocabulary() -> None:
    """Pattern sözlükte varsa → kendisi döner, mesafe 0."""
    mapped, distance = map_unseen_pattern("abc", {"abc", "bcc"})
    assert mapped == "abc"
    assert distance == 0


def test_map_unseen_pattern_single_vocabulary() -> None:
    """Sözlükte tek eleman varsa → o eleman döner."""
    mapped, distance = map_unseen_pattern("zzz", {"abc"})
    assert mapped == "abc"
    assert distance == levenshtein_distance("zzz", "abc")


def test_map_unseen_pattern_empty_vocabulary_raises() -> None:
    """Boş sözlük → ValueError fırlatmalı."""
    with pytest.raises(ValueError, match="vocabulary cannot be empty"):
        map_unseen_pattern("abc", set())


def test_map_unseen_pattern_multiple_equidistant() -> None:
    """Birden fazla eşit mesafeli pattern varsa → deterministik seçim."""
    # İki kez çağırınca aynı sonuç gelmeli (deterministik)
    result1, _ = map_unseen_pattern("adc", {"abc", "aec"})
    result2, _ = map_unseen_pattern("adc", {"abc", "aec"})
    assert result1 == result2


# ──────────────────────────────────────────────
# SAX Vocabulary & Unseen Generator Testleri
# ──────────────────────────────────────────────

def test_extract_sax_vocabulary_returns_unique() -> None:
    """Tekrar eden pattern'lar tek seferde sözlükte görünmeli."""
    patterns = ["abc", "abc", "bcc", "abc", "bcc", "aab"]
    vocab = extract_sax_vocabulary(patterns)
    assert vocab == {"abc", "bcc", "aab"}


def test_generate_unseen_patterns_not_in_vocabulary() -> None:
    """Üretilen pattern'lar sözlükte BULUNMAMALI."""
    vocabulary = {"abc", "bcc", "aab", "bbb", "aaa", "ccc"}
    unseen = generate_unseen_patterns(
        vocabulary=vocabulary,
        alphabet_size=3,
        window_size=3,
        n_unseen=5,
        seed=42,
    )
    for pattern in unseen:
        assert pattern not in vocabulary, f"'{pattern}' sözlükte bulunmamalıydı!"


def test_generate_unseen_patterns_correct_length() -> None:
    """Üretilen pattern uzunluğu window_size ile eşleşmeli."""
    vocabulary: set[str] = set()
    unseen = generate_unseen_patterns(
        vocabulary=vocabulary,
        alphabet_size=3,
        window_size=4,
        n_unseen=5,
        seed=42,
    )
    for pattern in unseen:
        assert len(pattern) == 4


def test_generate_unseen_patterns_count() -> None:
    """İstenen sayıda unseen pattern üretilmeli."""
    vocabulary: set[str] = set()
    unseen = generate_unseen_patterns(
        vocabulary=vocabulary,
        alphabet_size=4,
        window_size=3,
        n_unseen=8,
        seed=0,
    )
    assert len(unseen) == 8


# ──────────────────────────────────────────────
# Unseen Senaryo Entegrasyon Testi
# ──────────────────────────────────────────────

def test_create_unseen_scenario_injects_correctly() -> None:
    """
    Unseen senaryo: is_unseen listesindeki True olan indekslerdeki
    pattern'lar sözlükte bulunmamalı.
    """
    import numpy as np

    # Basit sinüs dalgası zaman serisi
    series = list(np.sin(np.linspace(0, 4 * np.pi, 200)))
    vocabulary = {"abc", "bcc", "aab", "bbb", "aaa", "ccc", "bca", "cab"}

    patterns, is_unseen = create_unseen_scenario(
        series=series,
        sax_vocabulary=vocabulary,
        alphabet_size=3,
        window_size=3,
        inject_ratio=0.1,
        seed=42,
    )

    # is_unseen listesi pattern listesiyle aynı uzunlukta olmalı
    assert len(patterns) == len(is_unseen)

    # Unseen olarak işaretlenen pattern'lar sözlükte bulunmamalı
    for i, (pattern, unseen_flag) in enumerate(zip(patterns, is_unseen)):
        if unseen_flag:
            assert pattern not in vocabulary, (
                f"İndeks {i}: '{pattern}' unseen işaretlendi ama sözlükte var!"
            )


def test_unseen_scenario_reproducible_with_seed() -> None:
    """Aynı seed ile aynı sonuç üretilmeli (reproducibility)."""
    import numpy as np

    series = list(np.sin(np.linspace(0, 2 * np.pi, 100)))
    vocabulary: set[str] = set()

    patterns1, is_unseen1 = create_unseen_scenario(
        series=series,
        sax_vocabulary=vocabulary,
        alphabet_size=3,
        window_size=3,
        seed=123,
    )
    patterns2, is_unseen2 = create_unseen_scenario(
        series=series,
        sax_vocabulary=vocabulary,
        alphabet_size=3,
        window_size=3,
        seed=123,
    )

    assert patterns1 == patterns2
    assert is_unseen1 == is_unseen2