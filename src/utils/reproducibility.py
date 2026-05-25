from __future__ import annotations

import random

import numpy as np


def set_random_seed(seed: int) -> None:
    """Set reproducibility seeds for supported libraries."""
    random.seed(seed)
    np.random.seed(seed)
