# Deliverable 2 - Static Analysis and Code Improvement

## Project

- Project: Python PySide6 Quiz App using the Open Trivia Database API
- Repository: jordanonlycodes/SQE-Quiz-App
- Branch: static-analysis
- Original source commit: ac648a2
- Baseline analysis commit: 91c1f2e
- Final analysis evidence commit: fc8dd51

## Full report

The complete report is [SQE_Static_Analysis_Report.pdf](SQE_Static_Analysis_Report.pdf) in this folder. It contains project selection, baseline analysis, ten investigated findings, A/B/C decisions, manual review, Pylint configuration, improvements, verification, comparison, limitations and evidence appendices.

This Markdown file is a summary and evidence index. The PDF contains the detailed investigation and original code examples.

## Results

| Metric | Baseline | Final | Change |
| --- | --- | --- | --- |
| Pylint score | 4.49/10 | 7.42/10 | +2.93 |
| Total findings | 695 | 434 | -261 |
| Errors | 90 | 15 | -75 |
| Warnings | 323 | 152 | -171 |
| Refactoring | 26 | 13 | -13 |
| Convention | 256 | 254 | -2 |
| Fatal | Not recorded | 0 | Not calculated |

Total findings decreased by approximately 37.6%. The change reflects code improvements and the documented Pylint configuration. Remaining findings are not automatically defects and need human review.

## Work completed

- Investigated W0201, W0718, R1720, R0913, R0917, R0902, R0801, W1514, C0123 and W0622.
- Fixed state initialization, unnecessary elif after raise, unspecified text encoding, exact type checking and the exit variable name.
- Split question transformation into smaller helpers and extracted repeated parameter-frame setup.
- Manually reviewed transformation responsibilities, repeated GUI setup, MainWindow coordination, startup responsibilities and overlap between unittest and pytest.
- Documented four Pylint settings: extension-pkg-allow-list=PySide6, disable=protected-access, good-names=tp and max-line-length=100. Broad warning, error and refactoring categories were not disabled.

## Recorded verification

- `python -m compileall -q main.py modules tests`: passed.
- `python -m unittest discover -s tests/unittest_backend -p 'test_*.py'`: 19 tests, 19 passed.
- Final Pylint analysis completed: 7.42/10 and 434 findings.
- The full GUI pytest suite could not complete because PySide6, pytest-mock and pytest-qt were unavailable.
- Application launch was blocked by missing PySide6. A successful GUI launch or GUI test pass is not claimed.

## Evidence files

| File | Contents |
| --- | --- |
| [deliverable1.md](deliverable1.md) | Project selection evidence |
| [SQE_Static_Analysis_Report.pdf](SQE_Static_Analysis_Report.pdf) | Complete final report |
| [pylint_baseline.txt](pylint_baseline.txt) | Original baseline console output |
| [../pylint_baseline.json](../pylint_baseline.json) | Original baseline JSON, stored at repository root |
| [pylint_final.txt](pylint_final.txt) | Final console output |
| [pylint_final.json](pylint_final.json) | Final JSON findings |
| [run_final_analysis.ps1](run_final_analysis.ps1) | Commands to repeat the final analysis |
| [../.pylintrc](../.pylintrc) | Project Pylint configuration |

The included .git directory preserves the original commit history. See the PDF for the meaning of each improvement commit and the limitations of static analysis.
