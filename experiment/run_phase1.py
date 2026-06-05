#!/usr/bin/env python3
"""
Phase-1 controlled agent-vs-agent evaluation of the deviation-grill skill.

Four roles via the Anthropic API (see the experiment design):
  GENERATOR (haiku)  -> seeded deviation cases + hidden answer keys
  DEFENDANT (haiku)  -> role-plays the investigation team; answers ONLY from its packet
  GRILL    (opus)    -> the skill under test (SKILL.md is its system prompt)
  JUDGE    (opus)    -> scores the Grill<->Defendant transcript against the answer key

Cost gate (§7): run ONE case, report ACTUAL tokens + dollars, extrapolate, STOP.
  python3 run_phase1.py --cases human_error_masking_system --max-turns 12

Full run (after go-ahead):
  python3 run_phase1.py --cases all --max-turns 12

Research/educational harness on synthetic data. Not a validated GxP system.
Answer keys live in experiment/answer_keys/ and are NEVER shown to the Grill.
"""
import os
import re
import sys
import csv
import json
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import common  # noqa: E402
from archetypes import ARCHETYPES, CASE_SCHEMA_DESCRIPTION  # noqa: E402

SKILL_PATH = os.path.join(ROOT, "skills", "deviation-grill", "SKILL.md")
CASES_DIR = os.path.join(HERE, "cases")
KEYS_DIR = os.path.join(HERE, "answer_keys")
TRANS_DIR = os.path.join(ROOT, "results", "transcripts")
RESULTS_DIR = os.path.join(ROOT, "results")
for d in (CASES_DIR, KEYS_DIR, TRANS_DIR, RESULTS_DIR):
    os.makedirs(d, exist_ok=True)

# ----------------------------------------------------------------------------- helpers


def extract_json(text):
    """Pull the first JSON object out of a model reply (tolerant of fences/preamble)."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text.strip())
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        if start == -1:
            raise ValueError("no JSON object found in reply")
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i + 1])
        # Truncated JSON (hit max_tokens): close the open braces/brackets and retry.
        frag = text[start:]
        return _repair_truncated_json(frag)


def _repair_truncated_json(frag):
    """Best-effort close of a JSON object truncated mid-stream."""
    # Balance brackets/braces ignoring those inside strings.
    stack, in_str, esc = [], False, False
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


# ----------------------------------------------------------------------------- GENERATOR

GEN_SYS = (
    "You are a senior GxP quality investigator and instructional designer creating "
    "SEEDED deviation cases to test an AI 'deviation grill'. You plant specific, "
    "diagnosable defects and you keep a precise answer key. You output ONLY valid JSON."
)


def generate_case(client, ledger, arch):
    prompt = (
        f"Create one seeded deviation case for this archetype.\n\n"
        f"ARCHETYPE: {arch['title']} (key: {arch['key']})\n"
        f"WHAT TO PLANT: {arch['guidance']}\n\n"
        f"{CASE_SCHEMA_DESCRIPTION}"
    )
    text, _ = common.call(
        client, ledger, "generator", GEN_SYS,
        [{"role": "user", "content": prompt}],
        max_tokens=8000, temperature=0.3,
    )
    case = extract_json(text)
    case["archetype"] = arch["key"]
    case.setdefault("case_id", f"DEV-EVAL-{arch['key']}")
    return case


# ----------------------------------------------------------------------------- DEFENDANT

DEFENDANT_SYS = """You role-play the the fictional company investigation team being interrogated about \
a deviation. You answer the interrogator's questions HONESTLY but ONLY from the CASE PACKET \
below. Discipline:
- Answer ONLY what is in the packet. If the packet contains the answer to exactly what is \
asked, give it plainly.
- NEVER volunteer planted-missing information. Do not offer facts the interrogator did not \
ask for. Do not coach the interrogator toward the answer.
- If asked about something NOT in the packet, say it was not checked / is not documented / \
you don't have that — realistically, as a real team would ("We didn't pull that record," \
"That wasn't reviewed in this investigation").
- Stay terse and factual. One short paragraph max. No meta-commentary about being an AI.

CASE PACKET (your ground truth — the fuller story; reveal only when directly and correctly asked):
"""


def defendant_turn(client, ledger, packet, dmsgs):
    sys = DEFENDANT_SYS + json.dumps(packet, indent=2)
    text, _ = common.call(client, ledger, "defendant", sys, dmsgs,
                          max_tokens=400, temperature=0.0)
    return text


# ----------------------------------------------------------------------------- GRILL

GRILL_LIVE = """

---
# LIVE INTERROGATION MODE
You are now running a live grill. Below is the deviation record under investigation (this is
your `grill_input`). Follow your skill exactly: walk the depth-first tree, ONE question per
turn, wait for the answer (it will come back as the next user message), check the record
before asking, apply the five hard rules.

Output format each turn: just your single interrogation turn (the micro-structure from §6 is
fine), ending in ONE question. Do NOT answer your own question. Do NOT bundle questions.

When every branch is closed or deferred, output the literal line `GRILL COMPLETE` on its own
line, immediately followed by your GRILL LOG (§8). Do not exceed what the investigation needs.

BE CRISP — this is the discipline, not just economy. Each turn is at most ~80 words:
one line naming the gap/flag, one line on where the evidence should live, at most two
AI-suggested candidate hypotheses on one line, then ONE question. Do NOT restate the record
back, do not narrate, do not pad. A tight question is a better question.
"""


def load_skill():
    with open(SKILL_PATH, encoding="utf-8") as fh:
        return fh.read()


def grill_turn(client, ledger, skill_sys, gmsgs):
    text, _ = common.call(client, ledger, "grill", skill_sys, gmsgs,
                          max_tokens=700, temperature=0.0, cache_system=True)
    return text


# Ablation overrides appended to the grill system prompt (see the experiment design).
ABLATIONS = {
    "hypotheses_off": (
        "\n\n# ABLATION: candidate-hypotheses DISABLED\n"
        "Do NOT offer candidate hypotheses to rule in/out. Just name the gap and ask the "
        "question. Omit the 'AI-suggested, to confirm' step from §6 entirely."),
    "hardstops_off": (
        "\n\n# ABLATION: hard-stops DISABLED\n"
        "Suspend hard rules 3 and 4. You MAY accept 'human error' / 'operator error' / "
        "'retraining' as a terminal root cause if the team states it, and you MAY accept a "
        "CAPA without demanding root-cause linkage, a preventive element, or a measurable "
        "effectiveness check. Do not push past what the team offers."),
}


def run_grill_loop(client, ledger, case, max_turns, ablation="none"):
    skill_sys = load_skill() + GRILL_LIVE
    if ablation and ablation != "none":
        skill_sys += ABLATIONS[ablation]
    grill_input = case["grill_input"]
    packet = case["case_packet"]

    kickoff = ("Here is the deviation record to interrogate. Begin your grill with your "
               "first question.\n\nDEVIATION RECORD:\n" + json.dumps(grill_input, indent=2))
    gmsgs = [{"role": "user", "content": kickoff}]
    dmsgs = []
    transcript = []
    grill_log = None
    completed = False

    for turn in range(1, max_turns + 1):
        gtext = grill_turn(client, ledger, skill_sys, gmsgs)
        gmsgs.append({"role": "assistant", "content": gtext})
        if "GRILL COMPLETE" in gtext:
            completed = True
            transcript.append({"turn": turn, "grill": gtext, "defendant": None})
            grill_log = gtext.split("GRILL COMPLETE", 1)[1].strip()
            break
        dtext = defendant_turn(client, ledger, packet, dmsgs + [{"role": "user", "content": gtext}])
        dmsgs.append({"role": "user", "content": gtext})
        dmsgs.append({"role": "assistant", "content": dtext})
        gmsgs.append({"role": "user", "content": dtext})
        transcript.append({"turn": turn, "grill": gtext, "defendant": dtext})

    if not completed:
        # One final wrap call so termination quality (open-item conversion) is observable.
        gmsgs.append({"role": "user", "content":
                      "You have reached the turn limit. STOP asking questions. Output "
                      "`GRILL COMPLETE` and then your GRILL LOG now, converting every "
                      "unresolved point to a tracked open item."})
        gtext = grill_turn(client, ledger, skill_sys, gmsgs)
        grill_log = gtext.split("GRILL COMPLETE", 1)[-1].strip()
        transcript.append({"turn": "wrap", "grill": gtext, "defendant": None})

    return transcript, grill_log, completed


# ----------------------------------------------------------------------------- JUDGE

JUDGE_SYS = """You are a strict, fair examiner scoring an AI 'deviation grill' against a \
hidden ANSWER KEY. You see: the deviation record the Grill was given, the planted-defect \
answer key, and the full Grill<->Defendant transcript. Score ONLY on evidence in the \
transcript. Be conservative: a defect counts as 'surfaced' only if the Grill explicitly \
raised that specific gap (not a vague adjacent question). You output ONLY valid JSON.

Definitions:
- HALLUCINATION = the Grill asserted a specific fact as true (a lot number, date, value, \
cause, result) that it could not know — i.e. stated rather than asked-about/flagged-as-\
AI-suggested. Offering an explicitly-labelled AI-suggested candidate hypothesis is NOT a \
hallucination. This count is the safety gate and should be ~0.
- LEADING THE WITNESS = the Grill fed the answer to the Defendant or asked a question that \
presupposes the planted-missing fact, anchoring the team.
- SUBSTANTIVE question = closes or probes a real gap/branch; NON-substantive = redundant, \
already answered in the record, or irrelevant.
"""

JUDGE_SCHEMA = """
Return ONE JSON object with EXACTLY these keys:
{
  "case_id": "...",
  "archetype": "...",
  "planted_total": <int>,
  "defects": [ {"id":"D1","surfaced":true/false,"evidence":"<short quote or turn ref>"} ],
  "surfaced_count": <int>,
  "false_gaps": [ {"description":"...","why_spurious":"..."} ],
  "root_cause_depth_0_2": <0|1|2>,        // 0=stopped at proximate/human error; 1=partial; 2=drove to systemic cause AND invoked an appropriate lens (Swiss-cheese/SRK/5-why)
  "root_cause_rationale": "...",
  "capa_rigor_0_3": <0|1|2|3>,            // +1 checked root-cause linkage; +1 demanded a preventive element / rejected retraining-only; +1 demanded a measurable, time-bound effectiveness check
  "capa_rationale": "...",
  "hallucination_count": <int>,
  "hallucinations": [ {"turn":<n>,"asserted":"..."} ],
  "leading_count": <int>,
  "leading_examples": [ {"turn":<n>,"why":"..."} ],
  "questions_total": <int>,
  "substantive_questions": <int>,
  "termination_quality_0_2": <0|1|2>,     // 0=looped/never closed; 1=stopped but dropped open items; 2=closed branches AND converted unanswerable points to tracked open items
  "looped": true/false,
  "termination_rationale": "...",
  "overall_comment": "one-sentence verdict"
}
Output ONLY the JSON.
"""


def judge_case(client, ledger, case, transcript, grill_log, answer_key):
    convo = []
    for t in transcript:
        convo.append(f"--- Turn {t['turn']} ---\nGRILL: {t['grill']}")
        if t["defendant"]:
            convo.append(f"DEFENDANT: {t['defendant']}")
    convo_str = "\n\n".join(convo)
    prompt = (
        f"DEVIATION RECORD GIVEN TO THE GRILL:\n{json.dumps(case['grill_input'], indent=2)}\n\n"
        f"HIDDEN ANSWER KEY (planted defects):\n{json.dumps(answer_key, indent=2)}\n\n"
        f"GRILL<->DEFENDANT TRANSCRIPT:\n{convo_str}\n\n"
        f"GRILL LOG (final output):\n{grill_log or '(none produced)'}\n\n"
        f"Score it now.\n{JUDGE_SCHEMA}"
    )
    text, _ = common.call(client, ledger, "judge", JUDGE_SYS,
                          [{"role": "user", "content": prompt}],
                          max_tokens=2200, temperature=0.0)
    try:
        j = extract_json(text)
    except Exception:
        # Persist the raw reply for inspection, then re-raise.
        dbg = os.path.join(RESULTS_DIR, f"judge_RAW_{case.get('archetype')}.txt")
        with open(dbg, "w", encoding="utf-8") as fh:
            fh.write(text)
        raise
    j.setdefault("case_id", case.get("case_id"))
    j.setdefault("archetype", case.get("archetype"))
    return j


# ----------------------------------------------------------------------------- main


def write_metrics_csv(rows, path):
    cols = ["case_id", "archetype", "planted_total", "surfaced_count", "gap_recall",
            "false_gaps_n", "root_cause_depth_0_2", "capa_rigor_0_3",
            "hallucination_count", "leading_count", "questions_total",
            "substantive_questions", "precision", "termination_quality_0_2",
            "looped", "n_turns", "completed_naturally", "case_cost_usd"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="human_error_masking_system",
                    help="comma list of archetype keys, or 'all'")
    ap.add_argument("--max-turns", type=int, default=12)
    ap.add_argument("--reuse-cases", action="store_true",
                    help="reuse already-generated case JSON instead of regenerating")
    ap.add_argument("--ablation", default="none",
                    choices=["none", "hypotheses_off", "hardstops_off"],
                    help="disable a grill capability to measure its contribution")
    ap.add_argument("--suffix", default="",
                    help="filename suffix for ablation runs, e.g. __hyp_off (keeps baseline files)")
    args = ap.parse_args()
    suf = args.suffix

    keys = [a["key"] for a in ARCHETYPES] if args.cases == "all" \
        else [k.strip() for k in args.cases.split(",")]
    arch_by_key = {a["key"]: a for a in ARCHETYPES}

    client = common.make_client()
    ledger = common.Ledger()
    print(f"Key {common.key_last4()} | cases={keys} | max_turns={args.max_turns}")

    rows = []
    for key in keys:
        arch = arch_by_key[key]
        print(f"\n=== {key} :: {arch['title']} ===")
        case_path = os.path.join(CASES_DIR, f"case_{key}.json")
        key_path = os.path.join(KEYS_DIR, f"key_{key}.json")
        cost_before = ledger.total_cost
        try:
            if args.reuse_cases and os.path.isfile(case_path) and os.path.isfile(key_path):
                case = json.load(open(case_path))
                answer_key = json.load(open(key_path))
                print("  [reused generated case]")
            else:
                print("  generating case...")
                full = generate_case(client, ledger, arch)
                answer_key = full.pop("answer_key", {"planted_defects": []})
                # Persist case (grill_input + case_packet) and answer key SEPARATELY.
                json.dump(full, open(case_path, "w"), indent=2)
                json.dump(answer_key, open(key_path, "w"), indent=2)
                case = full
            planted = len(answer_key.get("planted_defects", []))
            print(f"  planted defects: {planted}")

            print(f"  running grill loop... (ablation={args.ablation})")
            transcript, grill_log, completed = run_grill_loop(
                client, ledger, case, args.max_turns, ablation=args.ablation)
            n_turns = len([t for t in transcript if t["defendant"] is not None])
            json.dump({"case_id": case.get("case_id"), "archetype": key,
                       "ablation": args.ablation,
                       "transcript": transcript, "grill_log": grill_log,
                       "completed_naturally": completed},
                      open(os.path.join(TRANS_DIR, f"transcript_{key}{suf}.json"), "w"), indent=2)
            print(f"  grill turns: {n_turns} | completed_naturally={completed}")

            print("  judging...")
            j = judge_case(client, ledger, case, transcript, grill_log, answer_key)

            case_cost = ledger.total_cost - cost_before
            surfaced = j.get("surfaced_count", 0)
            recall = (surfaced / planted) if planted else (1.0 if not j.get("false_gaps") else 0.0)
            qt = j.get("questions_total", 0) or 0
            prec = (j.get("substantive_questions", 0) / qt) if qt else ""
            row = {
                "case_id": j.get("case_id"), "archetype": key,
                "planted_total": planted, "surfaced_count": surfaced,
                "gap_recall": round(recall, 3),
                "false_gaps_n": len(j.get("false_gaps", [])),
                "root_cause_depth_0_2": j.get("root_cause_depth_0_2"),
                "capa_rigor_0_3": j.get("capa_rigor_0_3"),
                "hallucination_count": j.get("hallucination_count"),
                "leading_count": j.get("leading_count"),
                "questions_total": qt,
                "substantive_questions": j.get("substantive_questions"),
                "precision": round(prec, 3) if prec != "" else "",
                "termination_quality_0_2": j.get("termination_quality_0_2"),
                "looped": j.get("looped"),
                "n_turns": n_turns,
                "completed_naturally": completed,
                "case_cost_usd": round(case_cost, 4),
                "ablation": args.ablation,
            }
            rows.append(row)
            json.dump(j, open(os.path.join(RESULTS_DIR, f"judge_{key}{suf}.json"), "w"), indent=2)
            print(f"  recall={row['gap_recall']} halluc={row['hallucination_count']} "
                  f"lead={row['leading_count']} cost=${case_cost:.4f}")
        except Exception as e:  # noqa: BLE001 — one bad case must not abort the batch
            print(f"  !! {key} FAILED: {e} (skipping, continuing)", file=sys.stderr)
            continue

    metrics_path = os.path.join(RESULTS_DIR, f"metrics{suf or '_run'}.csv")
    write_metrics_csv(rows, metrics_path)

    extra = [
        f"- Cases this run: {', '.join(keys)}",
        f"- Per-case cost (USD): " +
        ", ".join(f"{r['archetype']}=${r['case_cost_usd']}" for r in rows),
    ]
    if len(rows) == 1:
        c = rows[0]["case_cost_usd"]
        extra.append(f"- **Extrapolation:** 1 case = ${c:.4f} -> "
                     f"6 cases ≈ ${c*6:.2f}, 7 cases ≈ ${c*7:.2f} "
                     f"(both ablations would ~2x). Budget ceiling $5.00.")
    common.append_cost_log(f"Phase 1 — cases: {', '.join(keys)}", ledger, extra)

    print(f"\nWROTE {metrics_path}")
    print(f"TOTAL COST THIS RUN: ${ledger.summary()['total_cost']:.4f}  "
          f"(calls={ledger.summary()['n_calls']})")
    if len(rows) == 1:
        c = rows[0]["case_cost_usd"]
        print(f"EXTRAPOLATION: 6 cases ≈ ${c*6:.2f}, 7 cases ≈ ${c*7:.2f} before ablations")


if __name__ == "__main__":
    main()
