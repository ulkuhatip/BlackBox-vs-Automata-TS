"""
SAX (Symbolic Aggregate approXimation) Discretizer
---------------------------------------------------
This module transforms continuous numerical values (from PAA) into discrete 
textual symbols (letters) based on Gaussian distribution breakpoints.

Mathematical Logic:
-------------------
The real-valued space is divided into a equal-sized probability regions using 
Gaussian cut points \beta_1, \beta_2, ..., \beta_{a-1}.
- Region 1: (-\infty, \beta_1)        -> assigned to symbol 'a'
- Region 2: [\beta_1, \beta_2)         -> assigned to symbol 'b'
- Region i: [\beta_{i-1}, \beta_i)     -> assigned to symbol i-th alphabet character

Relation to Project Requirements (İsterler):
-------------------------------------------
- Satisfies Section VI & Section IX (Parametre Varyasyonu): Explicitly supports 
  the required Alphabet Size variation options (Değer = 3, 4, 5, 6).
"""

from __future__ import annotations
import numpy as np


class SAXDiscretizer:
    """Converts continuous numerical data into text sequences based on Gaussian breakpoints."""

    # Official statistical lookup table for Gaussian distribution breakpoints (a=3 to a=6)
    GAUSSIAN_BREAKPOINTS: dict[int, list[float]] = {
        3: [-0.43, 0.43],
        4: [-0.67, 0, 0.67],
        5: [-0.84, -0.25, 0.25, 0.84],
        6: [-0.97, -0.43, 0, 0.43, 0.97]
    }

    def __init__(self, alphabet_size: int = 3) -> None:
        """
        Args:
            alphabet_size (int): Total number of unique letters to use (3, 4, 5, or 6).
        """
        if alphabet_size not in self.GAUSSIAN_BREAKPOINTS:
            raise ValueError(f"Alphabet size must be 3, 4, 5, or 6. Got: {alphabet_size}")
            
        self.alphabet_size = alphabet_size
        self.breakpoints = self.GAUSSIAN_BREAKPOINTS[alphabet_size]
        
        # Generate lowercase alphabet characters string dynamically: e.g., ['a', 'b', 'c']
        self.alphabet = [chr(97 + i) for i in range(alphabet_size)]

    def discretize(self, paa_data: np.ndarray) -> list[str]:
        """
        Maps numerical array indices into discrete text characters.

        Args:
            paa_data (np.ndarray): Continuous data coming out of PAATransformer.

        Returns:
            list[str]: Array of character symbols.
        """
        symbols = []
        for value in paa_data:
            # np.digitize returns which Gaussian bucket the continuous value falls into
            bucket_idx = np.digitize(value, self.breakpoints)
            symbols.append(self.alphabet[bucket_idx])
            
        return symbols