from src.models.automata.transitions import build_transition_probabilities


def test_transition_probabilities_sum_per_source() -> None:
    probabilities = build_transition_probabilities({("a", "b"): 2, ("a", "c"): 2})
    assert probabilities[("a", "b")] == 0.5
    assert probabilities[("a", "c")] == 0.5
