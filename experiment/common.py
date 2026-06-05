"""
Shared harness utilities for the deviation-grill controlled evaluation.

- Loads ANTHROPIC_API_KEY from the environment, or from a secrets .env file pointed
  to by GRILL_SECRETS_ENV (an empty env var SHADOWS the .env value -> pop it first).
  The key value is NEVER printed (last-4 only, on request).
- Provides a single `call()` wrapper that records real token usage and dollar cost
  into a running tally, so the API budget is auditable.

Research/educational harness on synthetic data. Not a validated GxP system.
"""
import os
import sys
import json
import time

# Primary path is the ANTHROPIC_API_KEY env var. Optionally, a secrets .env file can be
# pointed to via the GRILL_SECRETS_ENV env var (default: ./secrets.env, gitignored).
SECRETS_ENV = os.path.expanduser(
    os.environ.get("GRILL_SECRETS_ENV",
                   os.path.join(os.path.dirname(__file__), "secrets.env"))
)

# Model tiering. Per user decision (2026-06-05): Opus GRILL + Sonnet JUDGE; Haiku for the
# cheap roles. Each is env-overridable so ablations / tier sweeps don't need code edits.
MODELS = {
    "grill": os.environ.get("GRILL_MODEL", "claude-opus-4-8"),
    "judge": os.environ.get("JUDGE_MODEL", "claude-sonnet-4-6"),
    "generator": os.environ.get("GENERATOR_MODEL", "claude-haiku-4-5-20251001"),
    "defendant": os.environ.get("DEFENDANT_MODEL", "claude-haiku-4-5-20251001"),
}

# Standard Anthropic list prices, USD per 1M tokens (input, output).
# Cost below is computed from REAL usage returned by the API; cache reads are
# billed at ~0.1x input and cache writes at ~1.25x input — accounted for explicitly.
PRICING = {
    "claude-opus-4-8":            {"in": 15.0, "out": 75.0, "cache_write": 18.75, "cache_read": 1.50},
    "claude-sonnet-4-6":          {"in": 3.0,  "out": 15.0, "cache_write": 3.75,  "cache_read": 0.30},
    "claude-haiku-4-5-20251001":  {"in": 1.0,  "out": 5.0,  "cache_write": 1.25,  "cache_read": 0.10},
}

COST_LOG = os.path.join(os.path.dirname(__file__), "..", "results", "cost_log.md")


def load_key():
    """Load ANTHROPIC_API_KEY from env or the secrets .env file. Never prints the value.
    An EMPTY env var SHADOWS the .env value, so it is popped first."""
    if os.environ.get("ANTHROPIC_API_KEY", "").strip() == "":
        os.environ.pop("ANTHROPIC_API_KEY", None)
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"]
    if not os.path.isfile(SECRETS_ENV):
        sys.exit(f"error: secrets file not found: {SECRETS_ENV}")
    with open(SECRETS_ENV, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == "ANTHROPIC_API_KEY":
                v = v.strip().strip('"').strip("'")
                if v:
                    os.environ["ANTHROPIC_API_KEY"] = v
                    return v
    sys.exit("error: ANTHROPIC_API_KEY not found in env or secrets file")


def key_last4():
    k = os.environ.get("ANTHROPIC_API_KEY", "")
    return f"...{k[-4:]}" if len(k) >= 4 else "(unset)"


class Ledger:
    """Accumulates token usage and dollar cost across all API calls."""
    def __init__(self):
        self.calls = []
        self.total_cost = 0.0

    def record(self, role, model, usage):
        p = PRICING[model]
        in_tok = getattr(usage, "input_tokens", 0) or 0
        out_tok = getattr(usage, "output_tokens", 0) or 0
        cw = getattr(usage, "cache_creation_input_tokens", 0) or 0
        cr = getattr(usage, "cache_read_input_tokens", 0) or 0
        cost = (in_tok * p["in"] + out_tok * p["out"]
                + cw * p["cache_write"] + cr * p["cache_read"]) / 1_000_000
        self.total_cost += cost
        rec = {"role": role, "model": model, "in": in_tok, "out": out_tok,
               "cache_write": cw, "cache_read": cr, "cost": round(cost, 6)}
        self.calls.append(rec)
        return rec

    def summary(self):
        return {"n_calls": len(self.calls), "total_cost": round(self.total_cost, 6)}


def make_client():
    load_key()
    import anthropic
    return anthropic.Anthropic()


def call(client, ledger, role, system, messages, max_tokens=1500,
         cache_system=False, temperature=0.0, model=None, retries=3):
    """One API call. `system` may be a string (optionally cache-controlled).
    Records usage to the ledger and returns the assistant text."""
    model = model or MODELS[role]
    sys_block = system
    if cache_system and isinstance(system, str):
        sys_block = [{"type": "text", "text": system,
                      "cache_control": {"type": "ephemeral"}}]
    kwargs = dict(model=model, max_tokens=max_tokens, system=sys_block, messages=messages)
    # Opus 4.8 deprecates the temperature parameter; only send it where supported.
    if not model.startswith("claude-opus-4-8"):
        kwargs["temperature"] = temperature
    last_err = None
    for attempt in range(retries):
        try:
            resp = client.messages.create(**kwargs)
            ledger.record(role, model, resp.usage)
            text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
            return text, resp
        except Exception as e:  # noqa: BLE001  (broad on purpose: backoff on any API error)
            last_err = e
            wait = 2 ** attempt
            print(f"  [retry {attempt+1}/{retries}] {role} call failed: {e} -> sleep {wait}s",
                  file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"{role} call failed after {retries} retries: {last_err}")


def append_cost_log(header, ledger, extra_lines=None):
    os.makedirs(os.path.dirname(COST_LOG), exist_ok=True)
    lines = [f"\n## {header}", "",
             f"- Key: {key_last4()}",
             f"- Calls: {ledger.summary()['n_calls']}",
             f"- **Total cost: ${ledger.summary()['total_cost']:.4f}**", ""]
    lines.append("| role | model | in | out | cache_w | cache_r | $ |")
    lines.append("|---|---|--:|--:|--:|--:|--:|")
    for c in ledger.calls:
        lines.append(f"| {c['role']} | {c['model']} | {c['in']} | {c['out']} | "
                     f"{c['cache_write']} | {c['cache_read']} | {c['cost']:.5f} |")
    if extra_lines:
        lines += [""] + list(extra_lines)
    with open(COST_LOG, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
