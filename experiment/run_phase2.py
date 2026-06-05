#!/usr/bin/env python3
"""
Phase 2 — run the deviation-grill on the real (synthetic) deviation records.

the experiment design: the records in investigation_data/particle_deviations.json are STRUCTURED
deviation records (not transcripts), so the Scribe is skipped and each record is ingested
directly and grilled. Because there is no live investigation team to answer back, the grill
runs in single-pass AUDIT MODE: it reviews the record and emits structured surfaced gaps +
summary flags (never fabricating facts; candidate hypotheses are AI-suggested).

Output: results/real_run.md — per-deviation surfaced gaps (categorized) + aggregate counts:
how many had human-error-only root causes flagged, retraining-only CAPAs, missing
effectiveness checks, unresolved conflicts.

  python3 run_phase2.py            # all records
  python3 run_phase2.py --n 8      # first 8 records

GRILL = Opus (the skill under test). One call per record (cached system prompt). No judge.
Research/educational output on synthetic data. Not a validated GxP system.
"""
import os
import sys
import json
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import common  # noqa: E402

DATA = os.path.expanduser("~/the fictional company/investigation_data/particle_deviations.json")
SKILL_PATH = os.path.join(ROOT, "skills", "deviation-grill", "SKILL.md")
RESULTS = os.path.join(ROOT, "results")
os.makedirs(RESULTS, exist_ok=True)

AUDIT_MODE = """

---
# AUDIT MODE (single-pass, no live team)
You are auditing a CLOSED structured deviation record. There is no team to answer back, so
instead of one-question-per-turn you do a single depth-first pass over the seven branches and
report what the investigation is MISSING or where its logic is WEAK. All five hard rules still
apply: interrogate the investigation not the person; never assert facts (point to where
evidence should live + offer AI-suggested candidate hypotheses); never accept human-error/
retraining as a terminal root cause; never let a CAPA pass without root-cause linkage + a
preventive element + a measurable, time-bound effectiveness check; unanswerable points become
tracked open items.

Return ONLY a JSON object:
{
  "deviation_id": "<from record>",
  "title": "<from record>",
  "summary_flags": {
    "human_error_only_root_cause": true/false,   // root cause stops at human/operator error w/o a system cause
    "retraining_only_capa": true/false,          // a CAPA whose only action is retrain/remind
    "missing_effectiveness_check": true/false,    // any CAPA lacks a measurable, time-bound effectiveness check
    "capa_not_linked_to_root_cause": true/false,
    "unresolved_conflict": true/false,           // contradictory statements/data left unresolved
    "scope_gap": true/false                      // other lots/products/timepoints not assessed
  },
  "surfaced_gaps": [
    {
      "branch": "problem_statement|containment|scope_impact|root_cause|capa|effectiveness|open_items",
      "category": "<short tag>",
      "gap": "<the specific weakness or missing item>",
      "where_evidence_lives": "<batch record / audit trail / cal data / training record / etc.>",
      "candidate_hypotheses": ["<AI-suggested, to confirm>", "..."],
      "severity": "patient_safety|product_quality|data_integrity|compliance"
    }
  ],
  "open_items": ["<unanswerable point converted to a tracked open item>"]
}
Output ONLY the JSON. No prose, no fences.
"""


def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        import re
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text.strip())
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        s = text.find("{")
        depth = 0
        for i in range(s, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[s:i + 1])
        # Truncated (hit max_tokens): balance open braces/brackets/strings and retry.
        frag, stack, in_str, esc = text[s:], [], False, False
        for ch in frag:
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch in "{[":
                stack.append(ch)
            elif ch in "}]":
                if stack:
                    stack.pop()
        if in_str:
            frag += '"'
        frag = frag.rstrip().rstrip(",")
        for opener in reversed(stack):
            frag += "}" if opener == "{" else "]"
        return json.loads(frag)


def render_markdown(audits):
    n = len(audits)
    def cnt(flag):
        return sum(1 for a in audits if a.get("summary_flags", {}).get(flag))
    L = []
    L.append("# Deviation-Grill — Phase 2: Run on Real (Synthetic) Deviation Records\n")
    L.append("> _Research/educational output on synthetic data "
             "(investigation_data/particle_deviations.json). Not a validated GxP system. The "
             "grill produces questions and AI-suggested hypotheses, never findings or facts._\n")
    L.append(f"\n**Records audited:** {n} structured deviation records (ingested directly; "
             "Scribe not needed). GRILL = claude-opus-4-8, single-pass audit mode.\n")
    L.append("\n## Aggregate — what the grill flagged across the corpus\n")
    L.append("| Flag | Records | % |")
    L.append("|---|--:|--:|")
    for flag, label in [
        ("human_error_only_root_cause", "Human-error-only root cause"),
        ("retraining_only_capa", "Retraining-only CAPA"),
        ("missing_effectiveness_check", "Missing/weak effectiveness check"),
        ("capa_not_linked_to_root_cause", "CAPA not linked to root cause"),
        ("unresolved_conflict", "Unresolved conflict / contradiction"),
        ("scope_gap", "Scope gap (other lots/timepoints)"),
    ]:
        c = cnt(flag)
        L.append(f"| {label} | {c}/{n} | {c/n:.0%} |")
    total_gaps = sum(len(a.get("surfaced_gaps", [])) for a in audits)
    total_open = sum(len(a.get("open_items", [])) for a in audits)
    L.append(f"\n- **Total surfaced gaps:** {total_gaps} (mean {total_gaps/n:.1f}/record)")
    L.append(f"- **Total tracked open items:** {total_open}")

    L.append("\n## Per-deviation detail\n")
    for a in audits:
        sf = a.get("summary_flags", {})
        flags_on = [k for k, v in sf.items() if v]
        L.append(f"\n### {a.get('deviation_id','?')} — {a.get('title','')}")
        L.append(f"_Flags:_ {', '.join(flags_on) if flags_on else 'none'}")
        gaps = a.get("surfaced_gaps", [])
        if gaps:
            L.append("\n| Branch | Category | Gap | Where evidence lives | Severity |")
            L.append("|---|---|---|---|---|")
            for g in gaps:
                L.append(f"| {g.get('branch','')} | {g.get('category','')} | "
                         f"{g.get('gap','')} | {g.get('where_evidence_lives','')} | "
                         f"{g.get('severity','')} |")
        if a.get("open_items"):
            L.append("\n_Open items:_")
            for oi in a["open_items"]:
                L.append(f"- {oi}")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0, help="number of records (0 = all)")
    ap.add_argument("--max-cost", type=float, default=3.3,
                    help="stop before starting a record if spend would exceed this (USD)")
    args = ap.parse_args()

    records = json.load(open(DATA))["deviations"]
    if args.n:
        records = records[:args.n]
    skill_sys = open(SKILL_PATH, encoding="utf-8").read() + AUDIT_MODE

    client = common.make_client()
    ledger = common.Ledger()
    print(f"Key {common.key_last4()} | auditing {len(records)} records")

    audits = []
    for i, rec in enumerate(records, 1):
        dev_id = rec.get("deviation_id", f"#{i}")
        if ledger.total_cost >= args.max_cost:
            print(f"  BUDGET GUARD: ${ledger.total_cost:.2f} >= ${args.max_cost} -> "
                  f"stopping after {i-1}/{len(records)} records.", flush=True)
            break
        print(f"  [{i}/{len(records)}] {dev_id} ... (spend ${ledger.total_cost:.2f})", flush=True)
        prompt = ("Audit this closed deviation record:\n\n" + json.dumps(rec, indent=2))
        text, _ = common.call(client, ledger, "grill", skill_sys,
                              [{"role": "user", "content": prompt}],
                              max_tokens=3000, temperature=0.0, cache_system=True)
        try:
            audit = extract_json(text)
        except Exception:
            with open(os.path.join(RESULTS, f"phase2_RAW_{dev_id}.txt"), "w") as fh:
                fh.write(text)
            print(f"     parse failed -> saved raw, skipping aggregate for {dev_id}")
            continue
        audit.setdefault("deviation_id", dev_id)
        audit.setdefault("title", rec.get("title", ""))
        audits.append(audit)

    json.dump(audits, open(os.path.join(RESULTS, "real_run_audits.json"), "w"), indent=2)
    with open(os.path.join(RESULTS, "real_run.md"), "w", encoding="utf-8") as fh:
        fh.write(render_markdown(audits))
    common.append_cost_log(f"Phase 2 — {len(audits)} real records", ledger)
    print(f"\nWROTE results/real_run.md ({len(audits)} records) | "
          f"cost ${ledger.summary()['total_cost']:.4f}")


if __name__ == "__main__":
    main()
