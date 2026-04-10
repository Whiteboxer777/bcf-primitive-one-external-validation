
#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import json, os, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Hard-coded known names
REMOVE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
}
REMOVE_FILE_SUFFIXES = {".pyc", ".pyo"}
REMOVE_FILE_NAMES = {".DS_Store"}


def _is_work_residue(path: Path) -> bool:
    """Any hidden directory ending with _tmp at project root is a work residue."""
    return (
        path.is_dir()
        and path.parent == ROOT
        and path.name.startswith('.')
        and path.name.endswith('_tmp')
    )

removed = {"dirs": [], "files": []}

# First pass: remove work-residue tmp dirs at project root
for child in sorted(ROOT.iterdir()):
    if _is_work_residue(child):
        shutil.rmtree(child, ignore_errors=True)
        removed["dirs"].append(str(child.relative_to(ROOT)))

# Second pass: remove pycache/pyc/DS_Store throughout tree
for path in sorted(ROOT.rglob("*"), key=lambda p: len(str(p)), reverse=True):
    if path.is_dir() and path.name in REMOVE_DIR_NAMES:
        shutil.rmtree(path, ignore_errors=True)
        removed["dirs"].append(str(path.relative_to(ROOT)))
    elif path.is_file() and (path.suffix in REMOVE_FILE_SUFFIXES or path.name in REMOVE_FILE_NAMES):
        try:
            path.unlink()
            removed["files"].append(str(path.relative_to(ROOT)))
        except FileNotFoundError:
            pass

remaining = []
for child in ROOT.iterdir():
    if _is_work_residue(child):
        remaining.append(str(child.relative_to(ROOT)))
for path in ROOT.rglob("*"):
    if path.is_dir() and path.name in REMOVE_DIR_NAMES:
        remaining.append(str(path.relative_to(ROOT)))
    elif path.is_file() and (path.suffix in REMOVE_FILE_SUFFIXES or path.name in REMOVE_FILE_NAMES):
        remaining.append(str(path.relative_to(ROOT)))

report = {
    "overall_ok": len(remaining) == 0,
    "removed": removed,
    "remaining_disallowed_artifacts": sorted(remaining),
}
(ROOT / "dist").mkdir(exist_ok=True)
(ROOT / "REPORTS").mkdir(exist_ok=True)
(ROOT / "dist" / "artifact_hygiene_factory_clean_report.json").write_text(json.dumps(report, indent=2))
(ROOT / "REPORTS" / "artifact_hygiene_factory_clean_report.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
