"""
Sliding Window Symbol Bundler
-----------------------------
This module processes an ordered stream of text symbols and extracts overlapping 
sub-sequences (words/patterns) using a sliding window strategy.

Mathematical Logic:
-------------------
Given an array of symbols S = [s_1, s_2, s_3, ..., s_m] and window size 'w':
    Pattern_1 = [s_1, s_2, ..., s_w]      (Combined as string: "s_1s_2...s_w")
    Pattern_2 = [s_2, s_3, ..., s_{w+1}]
    Pattern_i = [s_i, s_{i+1}, ..., s_{i+w-1}]

Relation to Project Requirements (İsterler):
-------------------------------------------
- Satisfies Section VI (Sliding Window): Directly converts the SAX letter sequence 
  into Automata States (Kelime/Pattern yapıları).
- Supports Section IX (Parametre Varyasyonu): Varies Window Size (Değer = 3, 4, 5, 6).
"""

from __future__ import annotations


class SlidingWindowBundler:
    """Slices character arrays into structured word sequences (States) for the Automata."""

    def __init__(self, window_size: int = 4) -> None:
        """
        Args:
            window_size (int): The sequence length of each word/state.
        """
        self.window_size = window_size

    def create_patterns(self, symbols: list[str]) -> list[str]:
        """
        Converts array of single letters into grouped string words.

        Args:
            symbols (list[str]): Continuous stream of characters e.g. ['a', 'b', 'b', 'c'].

        Returns:
            list[str]: Extracted overlapping state words e.g. ["abb", "bbc"].
        """
        patterns = []
        n = len(symbols)
        w = self.window_size

        if n < w:
            # Fallback protection: if array is too short, return the entire sequence as one word
            return ["".join(symbols)]

        # Move step-by-step extracting string words
        for i in range(n - w + 1):
            window_slice = symbols[i : i + w]
            word = "".join(window_slice)
            patterns.append(word)

        return patterns