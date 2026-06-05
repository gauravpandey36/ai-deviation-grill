#!/usr/bin/env python3
"""Aggregate all judged Phase-1 cases into the canonical results/metrics.csv + summary.md.

Reads every results/judge_<key>.json (baseline) and any results/judge_<key>__<ablation>.json,
joins each to its transcript (turn count, natural completion) and answer key (planted count),
computes the the experiment design metrics, and writes:
  - results/metrics.csv     (one row per case; baseline + ablation rows)
  - results/summary.md      (readable headline numbers + per-archetype table + ablation deltas)

Pure local aggregation — no API calls, no cost.
"""
import os
import csv
import json
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(ROOT, "results")
TRANS = os.path.join(RESULTS, "transcripts")
KEYS = os.path.join(HERE, "answer_keys")

COLS = ["case_id", "archetype", "variant", "planted_total", "surfaced_count", "gap_recall",
        "false_gaps_n", "root_cause_depth_0_2", "capa_rigor_0_3", "hallucination_count",
        "leading_count", "questions_total", "substantive_questions", "precision",
        "termination_quality_0_2", "looped", "n_turns", "completed_naturally"]


def load_rows():
    rows = []
    for jf in sorted(glob.glob(os.path.join(RESULTS, "judge_*.json"))):
        base = os.path.basename(jf)[len("judge_"):-len(".json")]
        # variant suffix is anything after a "__"
        if "__" in base:
            key, variant = base.split("__", 1)
        else:
            key, variant = base, "baseline"
        j = json.load(open(jf))
        tf = os.path.join(TRANS, f"transcript_{base}.json")
        tr = json.load(open(tf)) if os.path.isfile(tf) else {}
        n_turns = len([t for t in tr.get("transcript", []) if t.get("defendant") is not None])
        kf = os.path.join(KEYS, f"key_{key}.json")
        planted = len(json.load(open(kf)).get("planted_defects", [])) if os.path.isfile(kf) \
            else j.get("planted_total", 0)
        surfaced = j.get("surfaced_count", 0) or 0
        false_gaps = len(j.get("false_gaps", []) or [])
        recall = (surfaced / planted) if planted else (1.0 if false_gaps == 0 else 0.0)
        qt = j.get("questions_total", 0) or 0
        sq = j.get("substantive_questions", 0) or 0
        prec = round(sq / qt, 3) if qt else ""
        rows.append({
            "case_id": j.get("case_id"), "archetype": key, "variant": variant,
            "planted_total": planted, "surfaced_count": surfaced,
            "gap_recall": round(recall, 3), "false_gaps_n": false_gaps,
            "root_cause_depth_0_2": j.get("root_cause_depth_0_2"),
            "capa_rigor_0_3": j.get("capa_rigor_0_3"),
            "hallucination_count": j.get("hallucination_count"),
            "leading_count": j.get("leading_count"),
            "questions_total": qt, "substantive_questions": sq, "precision": prec,
            "termination_quality_0_2": j.get("termination_quality_0_2"),
            "looped": j.get("looped"), "n_turns": n_turns,
            "completed_naturally": tr.get("completed_naturally"),
        })
    return rows


def mean(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return round(sum(xs) / len(xs), 3) if xs else None


def write_summary(rows):
    base = [r for r in rows if r["variant"] == "baseline"]
    abl = [r for r in rows if r["variant"] != "baseline"]
    defective = [r for r in base if r["archetype"] != "thin_but_clean"]
    clean = [r for r in base if r["archetype"] == "thin_but_clean"]

    L = []
    L.append("# Deviation-Grill — Phase 1 Controlled Evaluation: Results Summary\n")
    L.append("> _Research/educational experiment on synthetic data. "
             "Not a validated GxP system. The grill produces questions and AI-suggested "
             "hypotheses, never findings or facts._\n")
    L.append(f"\n**Cases scored:** {len(base)} baseline archetypes"
             + (f" + {len(abl)} ablation runs" if abl else "") + ".\n")

    L.append("\n## Headline metrics (baseline, defect-bearing archetypes)\n")
    total_planted = sum(r["planted_total"] for r in defective)
    total_surfaced = sum(r["surfaced_count"] for r in defective)
    pooled_recall = round(total_surfaced / total_planted, 3) if total_planted else None
    L.append(f"- **Gap recall (pooled): {total_surfaced}/{total_planted} = "
             f"{pooled_recall:.1%}**" if pooled_recall is not None else "- Gap recall: n/a")
    L.append(f"- Mean per-case recall: {mean([r['gap_recall'] for r in defective])}")
    h_def = sum(r['hallucination_count'] or 0 for r in defective)
    h_clean = sum(r['hallucination_count'] or 0 for r in clean)
    L.append(f"- **Hallucinations (safety gate): {h_def} across {len(defective)} defect-bearing "
             f"cases; {h_clean} on the 1 clean case** — the safety gate holds when there is a "
             f"real defect, but the grill over-reaches and asserts unsupported facts on a "
             f"genuinely clean record")
    L.append(f"- Leading-the-witness: {sum(r['leading_count'] or 0 for r in base)} total")
    L.append(f"- Root-cause depth (0-2): mean {mean([r['root_cause_depth_0_2'] for r in defective])}")
    L.append(f"- CAPA rigor (0-3): mean {mean([r['capa_rigor_0_3'] for r in defective])}")
    L.append(f"- Question precision (substantive/total): mean {mean([r['precision'] for r in base])}")
    L.append(f"- Termination quality (0-2): mean {mean([r['termination_quality_0_2'] for r in base])}; "
             f"looped: {sum(1 for r in base if r['looped'])} of {len(base)}")
    if clean:
        c = clean[0]
        L.append(f"- **False-positive control (thin-but-clean):** {c['false_gaps_n']} "
                 f"manufactured gaps, {c['questions_total']} questions "
                 f"(a good grill stays quiet on a clean record)")

    L.append("\n## Per-archetype (baseline)\n")
    L.append("| Archetype | Planted | Surfaced | Recall | RC depth | CAPA | Halluc | Lead | Precision | Term | Turns | Closed |")
    L.append("|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--:|")
    for r in base:
        rec = "N/A" if r["planted_total"] == 0 else f"{r['gap_recall']:.0%}"
        L.append(f"| {r['archetype']} | {r['planted_total']} | {r['surfaced_count']} | "
                 f"{rec} | {r['root_cause_depth_0_2']} | {r['capa_rigor_0_3']} | "
                 f"{r['hallucination_count']} | {r['leading_count']} | "
                 f"{r['precision'] if r['precision']!='' else '—'} | "
                 f"{r['termination_quality_0_2']} | {r['n_turns']} | "
                 f"{'Y' if r['completed_naturally'] else 'N'} |")

    if abl:
        L.append("\n## Ablations (capability contribution)\n")
        L.append("| Archetype | Variant | Recall | RC depth | CAPA | Halluc | Lead |")
        L.append("|---|---|--:|--:|--:|--:|--:|")
        for r in sorted(abl, key=lambda x: (x["archetype"], x["variant"])):
            L.append(f"| {r['archetype']} | {r['variant']} | {r['gap_recall']:.0%} | "
                     f"{r['root_cause_depth_0_2']} | {r['capa_rigor_0_3']} | "
                     f"{r['hallucination_count']} | {r['leading_count']} |")
        L.append("\n_Compare each ablation row to its baseline row above to read the "
                 "capability's contribution._")

    with open(os.path.join(RESULTS, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


def main():
    rows = load_rows()
    rows.sort(key=lambda r: (r["variant"] != "baseline", r["archetype"], r["variant"]))
    with open(os.path.join(RESULTS, "metrics.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLS})
    write_summary(rows)
    print(f"aggregated {len(rows)} rows -> results/metrics.csv + results/summary.md")


if __name__ == "__main__":
    main()
