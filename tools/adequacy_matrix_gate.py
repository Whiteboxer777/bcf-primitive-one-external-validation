#!/usr/bin/env python3
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / 'SPEC' / 'ADEQUACY_MATRIX.md'
JSON_PATH = ROOT / 'SPEC' / 'ADEQUACY_MATRIX.json'
POLICY_PATH = ROOT / 'SPEC' / 'ADEQUACY_RELEASE_POLICY.json'
OUT_DIST = ROOT / 'dist' / 'adequacy_matrix_gate_report.json'
OUT_REPORTS = ROOT / 'REPORTS' / 'adequacy_matrix_gate_report.json'

PATH_TOKEN_RE = re.compile(r'`([^`]+)`|(?:(?<=\s)|^)([A-Za-z0-9_./*-]+\.(?:md|py|json|mjs|zip))(?!\S)')
ALIAS_EVIDENCE = {
    'theorem-family report': ['dist/theorem_family_corpus_report.json'],
    'adversarial report': ['dist/adversarial_closure_report.json'],
    'schema validation report': ['dist/schema_validation_report.json'],
    'equivalence report': ['dist/equivalence_report.json'],
    'independent parity report': ['dist/independent_second_implementation_parity_report.json'],
    'zip tree': ['SPEC/INDEX.md'],
    'source tree': ['src/bcf_primitive/runtime.py'],
    'verifier code path + adequacy row': ['src/bcf_primitive_verifier/verifier.py', 'SPEC/ADEQUACY_MATRIX.md'],
    'verifier code': ['src/bcf_primitive_verifier/verifier.py'],
    'schema files + verifier code': ['schemas/verification_result.schema.json', 'src/bcf_primitive_verifier/verifier.py'],
    'theorem-family + adversarial reports': ['dist/theorem_family_corpus_report.json', 'dist/adversarial_closure_report.json'],
    'theorem-family + adversarial + schema reports': ['dist/theorem_family_corpus_report.json', 'dist/adversarial_closure_report.json', 'dist/schema_validation_report.json'],
    'theorem-family + schema reports': ['dist/theorem_family_corpus_report.json', 'dist/schema_validation_report.json'],
    'theorem-family + equivalence reports': ['dist/theorem_family_corpus_report.json', 'dist/equivalence_report.json'],
    'theorem-family + independent parity + adversarial reports': ['dist/theorem_family_corpus_report.json', 'dist/independent_second_implementation_parity_report.json', 'dist/adversarial_closure_report.json'],
    'equivalence + parity + adversarial reports': ['dist/equivalence_report.json', 'dist/independent_second_implementation_parity_report.json', 'dist/adversarial_closure_report.json'],
}
HEADINGS_RE = re.compile(r'^(#+)\s+(.*)$')

STALE_PARTIAL_EXPECTATIONS = {
    "VF-07": "corpus/adversarial/verification_subfamilies/compiler_product_mismatch/cases.json",
    "VF-08": "corpus/adversarial/verification_subfamilies/certificate_invalidity/cases.json",
    "VF-09": "corpus/adversarial/verification_subfamilies/governance_invalidity/cases.json",
    "VF-10": "corpus/adversarial/verification_subfamilies/verdict_schema_tamper/cases.json",
    "VF-12": "corpus/adversarial/verification_subfamilies/refusal_schema_tamper/cases.json",
    "VF-13": "corpus/adversarial/verification_subfamilies/permit_schema_tamper/cases.json",
    "VF-14": "corpus/adversarial/verification_subfamilies/claim_tcb_tamper/cases.json",
}



def clean_cell(cell: str) -> str:
    cell = cell.strip()
    if cell.startswith('`') and cell.endswith('`'):
        cell = cell[1:-1]
    return cell


def parse_markdown_tables(path: Path):
    lines = path.read_text().splitlines()
    sections = []
    current = None
    i = 0
    while i < len(lines):
        m = HEADINGS_RE.match(lines[i])
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            if level == 1 and title and title[0].isdigit():
                current = {'title': title, 'tables': []}
                sections.append(current)
            i += 1
            continue
        if current is not None and lines[i].startswith('|') and i + 1 < len(lines) and lines[i+1].startswith('|---'):
            header = [clean_cell(c) for c in lines[i].strip().strip('|').split('|')]
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                parts = [clean_cell(c) for c in lines[i].strip().strip('|').split('|')]
                if len(parts) == len(header):
                    row = dict(zip(header, parts))
                    row['_section'] = current['title']
                    rows.append(row)
                i += 1
            current['tables'].append({'header': header, 'rows': rows})
            continue
        i += 1
    return sections


def extract_rows_from_sections(sections):
    summary_rows = []
    unit_rows = []
    gap_rows = []
    for section in sections:
        for table in section['tables']:
            header = table['header']
            rows = table['rows']
            if header == ['Family', 'Current line status', 'Exact meaning']:
                summary_rows.extend(rows)
            elif 'LAW_UNIT_ID' in header:
                unit_rows.extend(rows)
            elif 'GAP_ID' in header:
                gap_rows.extend(rows)
    return summary_rows, unit_rows, gap_rows


def path_tokens(text: str) -> List[str]:
    found = set()
    # direct regex matches
    for m in PATH_TOKEN_RE.finditer(text):
        token = (m.group(1) or m.group(2) or '').strip().strip('`').strip()
        if token and token not in {',', ', '}:
            found.add(token)
    # fallback split for comma-joined backtick artifacts from markdown parsing
    for part in re.split(r'[,;]', text):
        part = part.strip().strip('`').strip()
        if re.search(r'\.(md|py|json|mjs|zip)(?:$|\s)', part):
            token = re.search(r'([A-Za-z0-9_./*-]+\.(?:md|py|json|mjs|zip))', part)
            if token:
                found.add(token.group(1))
    return sorted(found)


def alias_tokens(text: str) -> List[str]:
    lowered = text.lower()
    out = []
    for phrase, tokens in ALIAS_EVIDENCE.items():
        if phrase in lowered:
            out.extend(tokens)
    return sorted(set(out))


def exists_token(token: str) -> bool:
    if '*' in token:
        return any(ROOT.glob(token))
    return (ROOT / token).exists()


def main() -> int:
    sections = parse_markdown_tables(MD_PATH)
    summary_rows, unit_rows, gap_rows = extract_rows_from_sections(sections)
    matrix_json = json.loads(JSON_PATH.read_text())
    policy = json.loads(POLICY_PATH.read_text())

    issues: List[str] = []
    warnings: List[str] = []
    status_vocab = set(policy['closed_status_vocabulary'])
    json_unit_rows = matrix_json.get('unit_rows', [])
    json_gap_rows = matrix_json.get('gap_rows', [])

    if len(unit_rows) != len(json_unit_rows):
        issues.append(f'Unit-row count mismatch: markdown={len(unit_rows)} json={len(json_unit_rows)}')
    if len(gap_rows) != len(json_gap_rows):
        issues.append(f'Gap-row count mismatch: markdown={len(gap_rows)} json={len(json_gap_rows)}')

    md_ids = [r['LAW_UNIT_ID'] for r in unit_rows]
    if len(md_ids) != len(set(md_ids)):
        issues.append('Duplicate LAW_UNIT_ID in markdown matrix.')

    json_ids = [r['LAW_UNIT_ID'] for r in json_unit_rows]
    if len(json_ids) != len(set(json_ids)):
        issues.append('Duplicate LAW_UNIT_ID in json matrix.')

    md_status_map = {r['LAW_UNIT_ID']: r['ADEQUACY_STATUS'] for r in unit_rows}
    json_status_map = {r['LAW_UNIT_ID']: r['ADEQUACY_STATUS'] for r in json_unit_rows}
    if md_status_map != json_status_map:
        issues.append('Markdown/json status maps differ.')

    # Validate statuses and release-blocking / allowed partials
    allowed_partial = set(policy['allowed_partial_ids'])
    blocking_prefixes = tuple(policy['release_blocking_prefixes'])
    full_rows_checked = []
    release_blocking_rows = []
    allowed_partial_rows_seen = []

    for row in unit_rows:
        row_id = row['LAW_UNIT_ID']
        status = row['ADEQUACY_STATUS']
        stale_partial_evidence = STALE_PARTIAL_EXPECTATIONS.get(row_id)
        if stale_partial_evidence and status == 'PARTIAL' and exists_token(stale_partial_evidence):
            issues.append(f"{row_id}: marked PARTIAL but dedicated adversarial evidence exists at {stale_partial_evidence}; matrix truth-sync required.")
        if status not in status_vocab:
            issues.append(f'{row_id}: illegal status {status}')
        if row_id.startswith(blocking_prefixes):
            release_blocking_rows.append(row_id)
            if status != 'FULL':
                issues.append(f'{row_id}: release-blocking row is not FULL (status={status}).')
        if status == 'PARTIAL':
            if row_id not in allowed_partial:
                issues.append(f'{row_id}: PARTIAL but not declared in allowed_partial_ids.')
            else:
                allowed_partial_rows_seen.append(row_id)
        if status in {'LAW_ONLY', 'MISSING'} and row_id.startswith(blocking_prefixes):
            issues.append(f'{row_id}: release-blocking row cannot be {status}.')
        # FULL rows must have some existing audit evidence tokens
        if status == 'FULL':
            full_rows_checked.append(row_id)
            tokens = sorted(set(path_tokens(row.get('AUDIT_EVIDENCE', '')) + alias_tokens(row.get('AUDIT_EVIDENCE', ''))))
            if not tokens:
                issues.append(f'{row_id}: FULL row has no concrete audit-evidence path tokens or aliases.')
            else:
                missing = [t for t in tokens if not exists_token(t)]
                if missing:
                    issues.append(f'{row_id}: FULL row references missing audit evidence: {missing}')

    for row_id in sorted(allowed_partial - set(allowed_partial_rows_seen)):
        warnings.append(f'Allowed PARTIAL id not present in current matrix: {row_id}')

    # required report artifacts
    report_results = {}
    for rel in policy['required_reports']:
        p = ROOT / rel
        if not p.exists():
            issues.append(f'Required report missing: {rel}')
            continue
        try:
            data = json.loads(p.read_text())
        except Exception as e:
            issues.append(f'Required report unreadable JSON: {rel}: {e}')
            continue
        overall = data.get('overall_ok', None)
        report_results[rel] = overall
        if overall is not None and overall is not True:
            issues.append(f'Required report overall_ok is not true: {rel} -> {overall}')

    # mirror consistency by row ids
    if md_ids != json_ids:
        issues.append('Markdown/json LAW_UNIT_ID order differs.')

    # write report
    report = {
        'overall_ok': not issues,
        'gate_name': 'adequacy_matrix_gate',
        'matrix_markdown': str(MD_PATH.relative_to(ROOT)),
        'matrix_json': str(JSON_PATH.relative_to(ROOT)),
        'policy': str(POLICY_PATH.relative_to(ROOT)),
        'counts': {
            'summary_rows': len(summary_rows),
            'unit_rows': len(unit_rows),
            'gap_rows': len(gap_rows),
            'release_blocking_rows': len(release_blocking_rows),
            'full_rows_checked': len(full_rows_checked),
        },
        'required_reports_checked': report_results,
        'issues': issues,
        'warnings': warnings,
    }
    OUT_DIST.write_text(json.dumps(report, indent=2) + '\n')
    OUT_REPORTS.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if not issues else 1


if __name__ == '__main__':
    raise SystemExit(main())
