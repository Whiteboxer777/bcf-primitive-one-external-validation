#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'tools' / 'external_truth_closure_gate.py'

def main() -> int:
    env = os.environ.copy()
    env['PYTHONPATH'] = str(ROOT / 'src')
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    proc = subprocess.run([sys.executable, str(TOOL)], cwd=ROOT, env=env, capture_output=True, text=True)
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip(), file=sys.stderr)
    return proc.returncode

if __name__ == '__main__':
    raise SystemExit(main())
