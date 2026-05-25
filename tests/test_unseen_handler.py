from src.models.automata.unseen_handler import levenshtein_distance
from src.models.automata.unseen_handler import map_unseen_pattern


def test_levenshtein_distance_exact_match() -> None:
    assert levenshtein_distance("abc", "abc") == 0


def test_map_unseen_pattern_returns_closest_pattern() -> None:
    mapped, distance = map_unseen_pattern("adc", {"abc", "bcc"})
    assert mapped == "abc"
    assert distance == 1
