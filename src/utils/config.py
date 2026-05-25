from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml_config(config_path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file into a dictionary."""
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def resolve_project_path(path_str: str | Path) -> Path:
    """Resolve a project-relative path into an absolute Path."""
    return Path(path_str).resolve()
