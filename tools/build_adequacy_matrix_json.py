#!/usr/bin/env python3
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / 'SPEC' / 'ADEQUACY_MATRIX.md'
JSON_PATH = ROOT / 'SPEC' / 'ADEQUACY_MATRIX.json'

HEADINGS_RE = re.compile(r'^(#+)\s+(.*)$')


def clean_cell(cell: str) -> str:
    cell = cell.strip()
    if cell.startswith('`') and cell.endswith('`'):
        cell = cell[1:-1]
    return cell


def parse_table(lines: List[str], start: int):
    header = [clean_cell(c) for c in lines[start].strip().strip('|').split('|')]
    rows = []
    i = start + 2
    while i < len(lines) and lines[i].startswith('|'):
        parts = [clean_cell(c) for c in lines[i].strip().strip('|').split('|')]
        if len(parts) == len(header):
            rows.append(dict(zip(header, parts)))
        i += 1
    return header, rows, i


def main() -> int:
    lines = MD_PATH.read_text().splitlines()
    sections: List[Dict[str, Any]] = []
    current = None
    i = 0
    while i < len(lines):
        m = HEADINGS_RE.match(lines[i])
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            if level == 1 and title[0].isdigit():
                current = {'title': title, 'tables': []}
                sections.append(current)
            i += 1
            continue
        if current is not None and lines[i].startswith('|') and not lines[i].startswith('|---'):
            if i + 1 < len(lines) and lines[i+1].startswith('|---'):
                header, rows, i = parse_table(lines, i)
                current['tables'].append({'header': header, 'rows': rows})
                continue
        i += 1

    unit_rows = []
    gap_rows = []
    summary_rows = []
    for section in sections:
        for table in section['tables']:
            header = table['header']
            rows = table['rows']
            if header == ['Family', 'Current line status', 'Exact meaning']:
                summary_rows.extend(rows)
            elif 'LAW_UNIT_ID' in header:
                for row in rows:
                    row['_section'] = section['title']
                    unit_rows.append(row)
            elif 'GAP_ID' in header:
                for row in rows:
                    row['_section'] = section['title']
                    gap_rows.append(row)

    data = {
        'matrix_version': 'executable_contract_v1',
        'source_markdown': str(MD_PATH.relative_to(ROOT)),
        'summary_rows': summary_rows,
        'unit_rows': unit_rows,
        'gap_rows': gap_rows,
        'counts': {
            'summary_rows': len(summary_rows),
            'unit_rows': len(unit_rows),
            'gap_rows': len(gap_rows),
        },
        'closed_status_vocabulary': ['FULL', 'PARTIAL', 'LAW_ONLY', 'MISSING', 'OUT_OF_SCOPE'],
    }
    JSON_PATH.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({'ok': True, 'json_path': str(JSON_PATH.relative_to(ROOT)), 'unit_rows': len(unit_rows), 'gap_rows': len(gap_rows)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
