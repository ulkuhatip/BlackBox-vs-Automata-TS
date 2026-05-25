from __future__ import annotations

import logging
from pathlib import Path


def get_logger(name: str, log_dir: str | Path = "outputs/logs") -> logging.Logger:
    """Create a simple file-backed logger."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path / f"{name}.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
