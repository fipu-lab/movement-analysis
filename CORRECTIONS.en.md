# CORRECTIONS.md — movement-analysis

Project: fipu-lab/movement-analysis
Base branch analyzed: master (commit e7863d7)
Destination fork: https://github.com/admeduardovieira/movement-analysis (created if it did not exist)

## Corrections proposed (not implemented yet — Phase 1 completed)

| ID | Title | Severity | Status | Risk | Files involved |
|----|-------|----------|--------|------|----------------|
| REA-001 | `fillna(0)` is not `inplace` nor assigned | P2 | PROPOSING | Low | `analysis.py` |
| REA-002 | `pattern.match(fname)` can return `None` → `AttributeError` | P2 | PROPOSING | Low | `analysis.py` |
| REA-003 | Access `record["active"]`/`record["inactive"]` without check → `KeyError` | P2 | PROPOSING | Low | `analysis.py` |
| REA-004 | README incomplete (cam3 missing) and hardcoded results | P3 | PROPOSING | Low | `README.md` |
| REA-005 | Inconsistent schema across CSVs | P3 | PROPOSING | Low | `data/*.csv` (documentation only) |
| REA-006 | No tests, CI, requirements.txt; Python 3.7 EOL | P3 | PROPOSING | Medium | `Pipfile`, `requirements.txt` (new), `tests/` (new), `.github/workflows/` (new) |

## Details of proposed corrections

### REA-001 — fillna(0) not persisted
**Problem:** `record.df.fillna(0)` does not modify the original DataFrame.  
**Correction:** change to `record.df.fillna(0, inplace=True)` or `record.df = record.df.fillna(0)`.  
**Validation test:** create a CSV with an empty/NaN `result` cell, run the script, and confirm there is no exception and the value is treated as 0.

### REA-002 — match can be None
**Problem:** a file in `data/` outside the pattern causes `AttributeError`.  
**Correction:** filter files with `if match is None: continue` before accessing `.group()`.  
**Validation test:** add a strange file to `data/` and confirm the script continues without error.

### REA-003 — missing groups cause KeyError
**Problem:** `record["active"]` / `record["inactive"]` without check.  
**Correction:** check that both keys exist before proceeding; otherwise print a warning and skip the camera.  
**Validation test:** create a `data/` folder with a camera that has only one group and confirm graceful behavior.

### REA-004 — incomplete README
**Problem:** README documents only cam1/cam2; cam3 exists in data. Hardcoded results.  
**Correction:** add cam3 section to README (or generate dynamically); keep a note that values are illustrative.  
**Validation test:** confirm README mentions cam1, cam2, and cam3.

### REA-005 — inconsistent schema across CSVs
**Problem:** `active_cam*` have filled `id`; `inactive_cam*` have empty `id`; `inactive_cam3` lacks `id`.  
**Correction:** document the variation in README; do not alter data (avoid destroying information). Consider standardizing in future collection.  
**Validation test:** confirm headers of all CSVs.

### REA-006 — reproducibility and CI base
**Problem:** no tests, no CI, no `requirements.txt`, Python 3.7 EOL.  
**Correction:** add `requirements.txt` (pandas, scipy), unit tests with pytest, GitHub Actions workflow, update `python_version` in `Pipfile` to 3.10+.  
**Validation test:** `pytest` passes; CI workflow runs on push/PR.

## Corrections to avoid due to lack of evidence
None of the above are avoided; all have technical evidence or are justified quality improvements. No changes are proposed without basis.

## Publication plan
- Create fork `admeduardovieira/movement-analysis`.
- Create branch `fix/rea-001-003-robustness` for REA-001..003.
- Create branch `docs/rea-004-readme` for REA-004.
- Commit with identity `admeduardovieira <admeduardovieira@users.noreply.github.com>`.
- Open PRs to `fipu-lab/movement-analysis` branch `master`.
- Add REVERSE_ENGINEERING_REPORT.md and CORRECTIONS.md + EN/UK translations to the fork.
