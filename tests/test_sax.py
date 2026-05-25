from src.features.sax import sax_transform


def test_sax_returns_string() -> None:
    result = sax_transform([0.1, 0.2, 0.3], 3)
    assert isinstance(result, str)
