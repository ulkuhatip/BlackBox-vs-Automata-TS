from src.features.paa import piecewise_aggregate_approximation


def test_paa_returns_requested_number_of_segments() -> None:
    result = piecewise_aggregate_approximation([1.0, 2.0, 3.0], 2)
    assert len(result) == 2
