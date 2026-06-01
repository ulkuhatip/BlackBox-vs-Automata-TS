from __future__ import annotations

from typing import Any


def _serialize_value(value: Any) -> Any:
    if isinstance(value, (str, bool, int, float)) or value is None:
        return value
    if isinstance(value, dict):
        return {key: _serialize_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    return str(value)


def format_decision_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a JSON-serializable explainability payload."""
    return {key: _serialize_value(value) for key, value in payload.items()}
