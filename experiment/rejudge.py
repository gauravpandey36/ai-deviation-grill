#!/usr/bin/env python3
"""Re-judge a saved Grill<->Defendant transcript WITHOUT re-running the (expensive) grill.

Loads results/transcripts/transcript_<key>.json + experiment/cases/case_<key>.json +
experiment/answer_keys/key_<key>.json, runs only the JUDGE, writes results/judge_<key>.json
and updates the metrics row. Cheap recovery path when a judge call fails to parse.

  python3 rejudge.py <archetype_key> [<archetype_key> ...]
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import common  # noqa: E402
import run_phase1 as rp  # noqa: E402


def main():
    keys = sys.argv[1:]
    if not keys:
        sys.exit("usage: python3 rejudge.py <archetype_key> [...]")
    client = common.make_client()
    ledger = common.Ledger()
    for key in keys:
        case = json.load(open(os.path.join(rp.CASES_DIR, f"case_{key}.json")))
        answer_key = json.load(open(os.path.join(rp.KEYS_DIR, f"key_{key}.json")))
        tr = json.load(open(os.path.join(rp.TRANS_DIR, f"transcript_{key}.json")))
        transcript, grill_log = tr["transcript"], tr.get("grill_log")
        print(f"re-judging {key} ...")
        j = rp.judge_case(client, ledger, case, transcript, grill_log, answer_key)
        json.dump(j, open(os.path.join(rp.RESULTS_DIR, f"judge_{key}.json"), "w"), indent=2)
        print(f"  recall {j.get('surfaced_count')}/{j.get('planted_total')} | "
              f"halluc {j.get('hallucination_count')} | lead {j.get('leading_count')} | "
              f"term {j.get('termination_quality_0_2')}")
    common.append_cost_log("Re-judge (transcript reuse)", ledger)
    print(f"re-judge cost: ${ledger.summary()['total_cost']:.4f}")


if __name__ == "__main__":
    main()
