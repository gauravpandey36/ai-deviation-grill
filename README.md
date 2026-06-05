# Deviation-Grill Experiment

An empirical test of whether an AI **"deviation grill"** — an agent that interrogates a pharma
GxP deviation investigation to expose missing evidence and weak root-cause logic — is worth
using. Built and measured end-to-end on **synthetic data**.

> _Research/educational experiment on generated data and a multi-agent harness. **Not a
> validated GxP system.** All examples use synthetic data generated for research and
> educational purposes for a fictional, deliberately-unnamed pharmaceutical company. No
> proprietary content from any current or prior employer is used or implied. The grill produces
> questions and AI-suggested hypotheses, never findings or facts._

## Attribution

The grill's interrogation discipline (one question at a time, walk the decision tree to closure)
is adapted from **Matt Pocock's `grill-me` skill** (MIT) —
<https://github.com/amazingloft999-droid/mattpocock-skills/blob/main/skills/productivity/grill-me/SKILL.md>.
The GxP guardrails, the deviation tree, and the evaluation harness are original. Full credit in
[`CREDITS.md`](CREDITS.md); this repo is MIT-licensed.

## The skill under test

`skills/deviation-grill/SKILL.md` — an investigation interrogator. One question per turn,
depth-first over 7 branches (problem statement → containment → scope/impact → root cause →
CAPA → effectiveness → open items). Five hard guardrails: interrogate the investigation not the
person; never assert facts; never accept "human error"/"retraining" as a terminal root cause;
never let a CAPA pass without root-cause linkage + a preventive element + a measurable, time-bound
effectiveness check; convert the genuinely-unanswerable to a tracked open item. It is the inverse
of the (separate) deviation-scribe extractor; the Scribe's gap flags are the Grill's input map.

## What was run

**Phase 1 — controlled agent-vs-agent eval** (`experiment/run_phase1.py`). Four roles:
GENERATOR (Haiku) plants known defects in seeded cases across 7 archetypes; DEFENDANT (Haiku)
role-plays the team, answering only from its packet; GRILL (Opus 4.8) is the skill under test;
JUDGE (Sonnet 4.6) scores the transcript against a hidden answer key. Answer keys live in
`experiment/answer_keys/` and are never shown to the Grill. Two ablations
(`--ablation hypotheses_off|hardstops_off`) measure capability contribution.

**Phase 2 — real-records run** (`experiment/run_phase2.py`). The Grill audits 13 of 16 structured
synthetic deviation records (`investigation_data/particle_deviations.json`) in single-pass mode.

## Headline results (full numbers in `results/`)

| Metric (Phase 1, 6 defect-bearing archetypes) | Result |
|---|---|
| Gap recall (planted defects surfaced) | **34/34 = 100%** |
| Root-cause depth (drove past human error) | 2/2 mean |
| CAPA rigor (linkage + prevention + effectiveness) | 3/3 mean |
| Hallucinations on defect cases | **1 total** |
| Question precision | ~0.92 |
| Termination (closed/deferred, never looped) | 2/2 mean |
| **Hallucinations on the 1 clean case** | **5 — manufactured 10 false gaps + fabricated facts** |

**The honest finding:** the safety gate holds when there is a real defect to find, and breaks on a
genuinely clean record — the grill over-reaches and asserts unsupported facts. Failure is legible
and located, which is engineerable. Use it as a supervised reviewer's-checklist generator, not as a
source of findings.

## Layout

```
skills/deviation-grill/SKILL.md   the skill under test
skills/deviation-scribe/          (placeholder — Scribe skipped; Phase-2 records are structured)
experiment/
  common.py          key loader (env / secrets file) + cost ledger + model tiering
  archetypes.py      7 seeded archetypes + case schema
  run_phase1.py      generator/defendant/grill/judge loop + ablations
  rejudge.py         cheap re-judge from a saved transcript (no re-grill)
  run_phase2.py      single-pass audit of real records (+ budget guard)
  aggregate.py       builds results/metrics.csv + results/summary.md
  cases/ answer_keys/ generated cases (answer keys isolated from the Grill)
results/
  metrics.csv summary.md          Phase-1 metrics
  real_run.md real_run_audits.json Phase-2 output + honest caveats
  transcripts/                     full grill<->defendant transcripts
  judge_*.json                     per-case judge scoring
  cost_log.md                      running API spend tally
deliverables/
  linkedin_article.md              write-up from actual results (charter-scanned PASS)
```

## Reproduce

```bash
cd experiment
python3 run_phase1.py --cases all --max-turns 12      # GENERATOR+DEFENDANT Haiku, GRILL Opus, JUDGE Sonnet
python3 aggregate.py
python3 run_phase1.py --cases human_error_masking_system --reuse-cases --ablation hypotheses_off --suffix __hyp_off
python3 run_phase1.py --cases human_error_masking_system --reuse-cases --ablation hardstops_off --suffix __hardstops_off
python3 run_phase2.py --max-cost 3.3
python3 aggregate.py
```

## Cost

Tiered models + prompt caching kept it affordable; Opus drove most of the cost. Total API spend
across all iterations (incl. debugging) ≈ **$14** real dollars; the clean post-fix run of the full
design (7 archetypes + 2 ablations + 13 real records) ≈ **$9.7**. Full per-call ledger in
`results/cost_log.md`.
