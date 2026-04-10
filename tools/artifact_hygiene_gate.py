from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'dist' / 'artifact_hygiene_gate_report.json'
FORBIDDEN_DIRS = {'__pycache__', '.pytest_cache'}
FORBIDDEN_SUFFIXES = {'.pyc', '.pyo'}
FORBIDDEN_NAMES = {'.DS_Store'}


def _is_work_residue(path: Path) -> bool:
    """Any hidden directory ending with _tmp at project root is a work residue."""
    return (
        path.is_dir()
        and path.parent == ROOT
        and path.name.startswith('.')
        and path.name.endswith('_tmp')
    )


def _factory_clean() -> dict:
    """Remove all known forbidden artifacts before scanning (self-healing)."""
    removed = {'dirs': [], 'files': []}
    # Pass 1: work-residue tmp dirs at root
    for child in sorted(ROOT.iterdir()):
        if _is_work_residue(child):
            shutil.rmtree(child, ignore_errors=True)
            removed['dirs'].append(str(child.relative_to(ROOT)))
    # Pass 2: forbidden dirs/files throughout tree (deepest first)
    for path in sorted(ROOT.rglob('*'), key=lambda p: len(str(p)), reverse=True):
        if path.is_dir() and path.name in FORBIDDEN_DIRS:
            shutil.rmtree(path, ignore_errors=True)
            removed['dirs'].append(str(path.relative_to(ROOT)))
        elif path.is_file() and (path.suffix in FORBIDDEN_SUFFIXES or path.name in FORBIDDEN_NAMES):
            try:
                path.unlink()
                removed['files'].append(str(path.relative_to(ROOT)))
            except FileNotFoundError:
                pass
    return removed


def main() -> int:
    # Step 1: Factory-clean — remove any artifacts left by prior Python execution
    cleaned = _factory_clean()

    # Step 2: Scan for anything that survived
    hits = []
    for child in sorted(ROOT.iterdir()):
        if _is_work_residue(child):
            hits.append({'path': str(child.relative_to(ROOT)), 'reason': 'work_residue_tmp_dir'})
    for path in ROOT.rglob('*'):
        rel = str(path.relative_to(ROOT))
        if any(part in FORBIDDEN_DIRS for part in path.parts):
            hits.append({'path': rel, 'reason': 'forbidden_dir'})
            continue
        if path.name in FORBIDDEN_NAMES:
            hits.append({'path': rel, 'reason': 'forbidden_name'})
            continue
        if path.suffix in FORBIDDEN_SUFFIXES:
            hits.append({'path': rel, 'reason': 'forbidden_suffix'})
    report = {
        'overall_ok': not hits,
        'forbidden_hits': hits,
        'forbidden_hit_count': len(hits),
        'factory_clean_performed': True,
        'factory_clean_removed': cleaned,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True), encoding='utf-8')
    return 0 if report['overall_ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
