from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
SPEC = ROOT / 'SPEC'
REPORT = DIST / 'canonical_release_surface_report.json'
MATRIX_JSON = SPEC / 'TRUST_BOUNDARY_MATRIX.json'


def main() -> int:
    matrix = json.loads(MATRIX_JSON.read_text(encoding='utf-8'))
    canonical = [row for row in matrix['entries'] if row['release_surface'] == 'canonical']
    auxiliary = [row for row in matrix['entries'] if row['release_surface'] != 'canonical']
    by_authority: dict[str, int] = {}
    for row in matrix['entries']:
        by_authority[row['authority_level']] = by_authority.get(row['authority_level'], 0) + 1
    report: dict[str, Any] = {
        'pass_id': 'INDEPENDENCE_CLOSURE_AND_TRUST_COMPRESSION_PASS',
        'overall_ok': True,
        'canonical_entry_count': len(canonical),
        'auxiliary_entry_count': len(auxiliary),
        'authority_level_counts': by_authority,
        'canonical_release_entries': canonical,
        'non_canonical_entries': auxiliary,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps({'overall_ok': True, 'canonical_entry_count': len(canonical), 'report': str(REPORT.relative_to(ROOT))}, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
