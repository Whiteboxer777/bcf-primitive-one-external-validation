from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

PRIMITIVE_IDENTITY = 'BCF Primitive One'


def canonical_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def digest_data(data: Any) -> str:
    return hashlib.sha256(canonical_bytes(data)).hexdigest()


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
