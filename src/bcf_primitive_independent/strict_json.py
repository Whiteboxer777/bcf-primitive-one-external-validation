"""Independent strict JSON parser for the second implementation line."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StrictParseError(ValueError):
    pass


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise StrictParseError(f'duplicate JSON key: {key}')
        out[key] = value
    return out


def loads_strict(text: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicates)
    except json.JSONDecodeError as exc:
        raise StrictParseError(str(exc)) from exc


def load_path_strict(path: str | Path) -> Any:
    return loads_strict(Path(path).read_text(encoding='utf-8'))
