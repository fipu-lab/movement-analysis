# REVERSE_ENGINEERING_REPORT — movement-analysis

## A. General diagnosis

### Architecture identified
Minimal Python project for statistical movement analysis. No application layer, API, interface, or database. The flow is a single script `analysis.py` that:

1. Reads all CSV files in the `data/` folder whose name matches the pattern `(?P<type>.*)_(?P<cam>.*)_formula.csv`.
2. Loads each CSV into a pandas DataFrame.
3. Groups records by camera (`cam`) and type (`active` / `inactive`).
4. For each camera, applies the Mann-Whitney U test (`scipy.stats.mannwhitneyu`, `alternative="greater"`) comparing the `result` columns of active and inactive groups.
5. Prints counts, quantiles, and the test result.

There is no web entry point, no routes, no frontend component. It is an offline analysis script.

### Technologies and dependencies
- Language: Python 3.7 (declared in `Pipfile`, already end-of-life)
- Runtime dependencies: `pandas`, `scipy`
- Dev dependencies: `black`, `ipython`, `ipykernel`
- Manager: Pipenv (`Pipfile` + `Pipfile.lock` committed)
- No `requirements.txt`, no `setup.py`/`pyproject.toml`, no CI configured.

### Maintenance state
Last commit: `e7863d7 Update README.md`. Short history (4 commits). Upstream default branch: `master`. Upstream repository: `https://github.com/fipu-lab/movement-analysis`. No relevant recent issues or PR activity. Low-activity project.

### Existing testing mechanisms
No automated tests found. No `tests/` folder, no `test_*.py` file, no pytest configuration. No CI/CD (`.github/workflows` folder does not exist).

### Investigation limitations
- REA 6.7.0 not operational via CLI in this environment (the `rea` file is a PulsoGold environment link/document, not a standalone executable; execution blocked). Analysis performed through static code inspection + data reading + terminal.
- pandas/scipy not installed in the available Python interpreters; heavy download avoided per instruction. README numeric results were not reproduced by execution, only confronted with CSV line counts.
- No access to private data; only synthetic/public data already present in the repository was used.

## B. Problems found

| ID | Title | Severity | Status | Location |
|----|-------|----------|--------|----------|
| REA-001 | `fillna(0)` is not `inplace` nor assigned | P2 | PROBABLE | `analysis.py:16` |
| REA-002 | `pattern.match(fname)` can return `None` → `AttributeError` | P2 | PROBABLE | `analysis.py:17-19` |
| REA-003 | Access `record["active"]`/`record["inactive"]` without check → `KeyError` | P2 | PROBABLE | `analysis.py:26-28` |
| REA-004 | README documents only cam1/cam2; cam3 data exists; hardcoded results | P3 | CONFIRMED | `README.md`, `data/` |
| REA-005 | Inconsistent schema across CSVs (`id` column filled/empty/absent) | P3 | CONFIRMED | `data/*.csv` |
| REA-006 | Missing tests, CI, requirements.txt; Python 3.7 EOL | P3 | CONFIRMED | `Pipfile`, repo root |

### Details of confirmed problems

**REA-004 (CONFIRMED)**: `README.md` records analyses only for `cam1` and `cam2`, but the `data/` folder contains `active_cam3_formula.csv` and `inactive_cam3_formula.csv` (25,779 lines each). The script `analysis.py` would process cam3 if executed, but the README does not mention it. Additionally, the `pvalue` and `statistic` values in the README are hardcoded (e.g. `pvalue=0.0` for cam1), not automatically reproducible from the code.

Evidence: `README.md:7-27` mentions only cam1/cam2; `data/` contains 6 files including cam3.

**REA-005 (CONFIRMED)**: CSVs do not share the same schema. `active_cam1/2/3` have columns `timestamp,id,result` with `id` filled. `inactive_cam1/2` have `timestamp,id,result` with empty `id` (`,,value`). `inactive_cam3` has only `timestamp,result` (no `id` column). The script reads only `result`, so it does not break, but it is a data inconsistency.

Evidence: header of `inactive_cam3_formula.csv` = `timestamp,result`; header of `active_cam1_formula.csv` = `timestamp,id,result`.

**REA-006 (CONFIRMED)**: No automated tests, no CI, no `requirements.txt`. The `Pipfile` declares `python_version = "3.7"` (end of life since 2023-06-27).

### Details of probable problems (not reproduced in current data)

**REA-001 (PROBABLE)**: `record.df.fillna(0)` (line 16) does not pass `inplace=True` nor assign the result back (`record.df = record.df.fillna(0)`). The default `fillna` returns a new DataFrame. If `result` contained `NaN`, they would not be filled and `mannwhitneyu` could fail or return `NaN`. In current CSVs the `result` column is filled, so it does not manifest, but it is a latent bug.

**REA-002 (PROBABLE)**: `match = pattern.match(fname)` (line 17). If any file in `data/` does not match the pattern `.*_.*_formula.csv` (e.g. `.DS_Store`, `README`, temporary file), `match` will be `None` and `match.group("type")` will raise `AttributeError`, interrupting the whole script. No file filtering or exception handling exists.

**REA-003 (PROBABLE)**: Lines 26-28 access `record["active"]` and `record["inactive"]` directly. If a camera has only one group (e.g. only `active`), a `KeyError` occurs.

## C. Recurring problems
No recurring public issues or PRs found for this repository (very low activity, short history). No documented regressions.

## D. Undocumented errors
All items in section B are problems not previously documented by the project (no related issue/PR found).

## E. Performance
No significant performance opportunities identified: the script processes a modest volume of data (maximum ~52k lines per file) in memory, once. No nested loops, network requests, or re-renders. Reading all CSVs into nested dictionaries is adequate for the scope.

## F. Technical improvements
- Apply `inplace=True` or reassignment on `fillna(0)` (REA-001).
- Filter only files matching the pattern and handle `match is None` (REA-002).
- Check existence of both groups before accessing them (REA-003).
- Update README to include cam3 and/or generate results dynamically (REA-004).
- Standardize CSV schema or document the variation (REA-005).
- Add `requirements.txt`, unit tests with `pytest`, GitHub Actions CI, update Python version in `Pipfile` (REA-006).

## G. Execution plan
Independent, low-risk corrections (can be separate PRs):
1. REA-001, REA-002, REA-003 — `analysis.py` robustness (low risk, reproducible test).
2. REA-004 — README update.
3. REA-005 — data schema documentation/standardization.
4. REA-006 — `requirements.txt`, tests, CI, Python version (more involved).

All are independent of each other.

## H. Expected outcome
Make the script robust to unexpected inputs (strange files, missing groups, NaN), document all cameras correctly, and establish a testable basis for future contributions.

---

**Tools used:** git, gh (authenticated as admeduardovieira), PowerShell/terminal, static code inspection.  
**Limitation:** REA 6.7.0 not operational in this environment; pandas/scipy not installed (numeric execution not performed).  
**Environment:** Windows, PowerShell 5.1, `C:\Users\User\audit-repos\movement-analysis` (clone of upstream, branch `master`, commit `e7863d7`).
