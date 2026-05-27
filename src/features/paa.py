"""
PAA (Piecewise Aggregate Approximation) Transformer
---------------------------------------------------
This module implements the PAA dimensionality reduction technique for time series.
It divides a continuous 1D numerical signal (such as PC1) into equal-sized frames 
and calculates the arithmetic mean for each frame.

Mathematical Formula:
---------------------
Given a time series X of length n, PAA reduces it to a vector Y of length w:
    Y_i = (w / n) * \sum_{j = (n/w)(i-1) + 1}^{(n/w)i} X_j

Relation to Project Requirements (İsterler):
-------------------------------------------
- Satisfies Section VI (Automata Model İç Yapısı): PAA is strictly required 
  as the foundational data reduction layer before applying SAX discretization.
"""

from __future__ import annotations
import numpy as np
import pandas as pd


class PAATransformer:
    """Compresses a continuous time series using Piecewise Aggregate Approximation."""

    def __init__(self, window_size: int = 4) -> None:
        """
        Args:
            window_size (int): The size of the local aggregation window (w).
        """
        self.window_size = window_size

    def transform(self, series: pd.Series | np.ndarray) -> np.ndarray:
        """
        Transforms a 1D numerical sequence into its PAA representation.
        
        Args:
            series: Input 1D numerical data (e.g., final_train['PC1']).
            
        Returns:
            np.ndarray: The compressed/smoothed numerical time series.
        """
        # Convert pandas Series to numpy array if necessary
        data = np.asarray(series, dtype=np.float64)
        n = len(data)
        w = self.window_size

        # If the data length matches window size or is shorter, return as is
        if n <= w:
            return data

        # Calculate the number of equal-sized blocks
        num_blocks = n // w
        
        # Reshape and compute the mean for each block (vectorized for speed)
        truncated_data = data[:num_blocks * w]
        paa_rep = truncated_data.reshape(-1, w).mean(axis=1)

        # Handle remaining data points at the tail if any (edge case protection)
        if n % w != 0:
            remainder_mean = np.mean(data[num_blocks * w:])
            paa_rep = np.append(paa_rep, remainder_mean)

        return paa_rep