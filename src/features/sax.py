from __future__ import annotations

from typing import Sequence


def sax_transform(values: Sequence[float], alphabet_size: int) -> str:
    """Placeholder SAX encoding."""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return "".join(alphabet[min(index, alphabet_size - 1)] for index, _ in enumerate(values))
