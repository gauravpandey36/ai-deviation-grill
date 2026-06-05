# Deviation-Grill — Phase 1 Controlled Evaluation: Results Summary

> _Research/educational experiment on synthetic data. Not a validated GxP system. The grill produces questions and AI-suggested hypotheses, never findings or facts._


**Cases scored:** 7 baseline archetypes + 2 ablation runs.


## Headline metrics (baseline, defect-bearing archetypes)

- **Gap recall (pooled): 34/34 = 100.0%**
- Mean per-case recall: 1.0
- **Hallucinations (safety gate): 1 across 6 defect-bearing cases; 5 on the 1 clean case** — the safety gate holds when there is a real defect, but the grill over-reaches and asserts unsupported facts on a genuinely clean record
- Leading-the-witness: 11 total
- Root-cause depth (0-2): mean 2.0
- CAPA rigor (0-3): mean 3.0
- Question precision (substantive/total): mean 0.915
- Termination quality (0-2): mean 2.0; looped: 0 of 7
- **False-positive control (thin-but-clean):** 10 manufactured gaps, 12 questions (a good grill stays quiet on a clean record)

## Per-archetype (baseline)

| Archetype | Planted | Surfaced | Recall | RC depth | CAPA | Halluc | Lead | Precision | Term | Turns | Closed |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--:|
| data_integrity_alcoa | 7 | 7 | 100% | 2 | 3 | 1 | 1 | 1.0 | 2 | 8 | Y |
| equipment_calibration | 5 | 5 | 100% | 2 | 3 | 0 | 1 | 0.909 | 2 | 11 | Y |
| human_error_masking_system | 6 | 6 | 100% | 2 | 3 | 0 | 1 | 1.0 | 2 | 8 | Y |
| material_supplier | 6 | 6 | 100% | 2 | 3 | 0 | 2 | 0.833 | 2 | 11 | Y |
| planted_conflict | 5 | 5 | 100% | 2 | 3 | 0 | 2 | 1.0 | 2 | 9 | Y |
| procedure_ambiguity | 5 | 5 | 100% | 2 | 3 | 0 | 2 | 0.833 | 2 | 12 | N |
| thin_but_clean | 0 | 0 | N/A | 2 | 3 | 5 | 2 | 0.833 | 2 | 11 | Y |

## Ablations (capability contribution)

| Archetype | Variant | Recall | RC depth | CAPA | Halluc | Lead |
|---|---|--:|--:|--:|--:|--:|
| human_error_masking_system | hardstops_off | 100% | 2 | 3 | 0 | 1 |
| human_error_masking_system | hyp_off | 100% | 2 | 3 | 1 | 0 |

_Compare each ablation row to its baseline row above to read the capability's contribution._
