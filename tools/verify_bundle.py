from __future__ import annotations

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import json
from bcf_primitive_verifier.verifier import verify_bundle

if __name__ == "__main__":
    print(json.dumps(verify_bundle(sys.argv[1]), indent=2, sort_keys=True))
