# I built an AI "deviation grill" and tried to prove it was useless. Here's what the numbers actually said.

A deviation investigation lives or dies on the questions nobody asked. The missing scope check. The "human error" that was really an ambiguous SOP. The CAPA with no effectiveness check. I wanted to know whether an AI interrogator — one that does nothing but *pressure-test* an investigation — earns its place in a quality workflow, or whether it's another confident hallucination machine you can't put near a GxP record.

So I built one and ran a controlled experiment to try to break it. Here's what happened — including where it failed.

## What the "grill" is

It's a single-purpose interrogator. Not a writer, not a summarizer. It walks an investigation as a depth-first tree — problem statement → containment → scope/impact → root cause → CAPA → effectiveness → open items — and asks **one question at a time**. It runs on five hard rules:

1. Interrogate the **investigation**, never the person.
2. **Never assert facts.** It can't invent a lot number or a cause. It can only point to where the evidence should live (batch record, audit trail, calibration data, training records) and offer clearly-labelled *AI-suggested* hypotheses to rule in or out.
3. **Never accept "human error" or "retraining"** as a terminal root cause — drive to the system condition that allowed it.
4. **Never let a CAPA pass** without a root-cause linkage, a preventive element, and a measurable, time-bound effectiveness check.
5. Anything genuinely unanswerable becomes a tracked **open item**, never silently dropped.

## How I tested it (in plain English)

Four AI agents, kept honest by isolation:

- A **generator** wrote synthetic deviation cases across seven archetypes (human-error-masking-a-system-cause, equipment/calibration, material/supplier, procedure ambiguity, data-integrity/ALCOA, a planted speaker conflict, and one *thin-but-genuinely-clean* case) — and planted a known list of defects in each, kept in an answer key the grill never saw.
- A **defendant** role-played the investigation team, answering only from its case packet and never volunteering the missing information.
- The **grill** interrogated the defendant.
- A **judge** scored the transcript against the hidden answer key.

Then I ran the grill on 13 of my own (synthetic) structured deviation records.

Everything is synthetic data from a fictional company. This is a research experiment, not a validated GxP system.

## What the numbers said

**On cases with real, planted defects, it was strong:**

- **34 of 34 planted defects surfaced — 100% gap recall** across the six defect-bearing archetypes.
- **Root-cause depth: 2/2.** On every case it refused to stop at "operator error" and drove to the latent system condition, naming the lens it used (Swiss-cheese, skills-rules-knowledge).
- **CAPA rigor: 3/3.** It rejected retraining-only CAPAs on all three counts — linkage, prevention, and a measurable effectiveness check.
- **Question precision ~0.92**, and it **never looped** — it closed branches or converted them to tracked open items and stopped.

**And then it failed exactly where it matters most.**

On the one case that was *genuinely clean* — nothing wrong, a correct systemic root cause, a real effectiveness check — the grill **manufactured 10 gaps that didn't exist and asserted 5 fabricated facts**: it invented a prior deviation number, made up cycle-rate data, and cited vendor "specifications" that were nowhere in the record. Across the six defect cases there was 1 hallucination total. On the clean case there were five.

That's the whole finding in one line: **the safety gate holds when there's something to find, and breaks when there isn't.** A tool that can't tell "clean" from "I'll invent a problem" is a tool you supervise, not one you trust.

**Two ablations** (turning off the candidate-hypotheses and the hard-stop guardrails) didn't degrade a clearly-systemic case — but that was a single case, so I won't over-read it. The honest version: I can't yet show what the guardrails buy you on subtle cases.

**On my 13 real records,** it averaged ~8 surfaced gaps per record and flagged human-error-only root causes and retraining-only CAPAs in ~15% each. But the eye-catching "100% missing effectiveness check" number is mostly an **input artifact** — the records reference CAPAs by ID without embedding the CAPA text, so the grill correctly reported it *couldn't verify* them, not that they were all broken. Worth saying plainly, because the inflated number is the kind of thing that gets quoted out of context.

## What I'd actually do with it

- **Good at:** generating a reviewer's checklist of what an investigation is missing; refusing lazy "human error" closures; forcing CAPA discipline; staying on-method without rambling.
- **Where it fails:** a clean record. It over-reaches and — worse — states unsupported facts. For a GxP tool, asserting a fact it can't know is the cardinal sin.
- **What I would not trust it with:** its output as *findings*; judging CAPA adequacy without the linked CAPA records in front of it; running unsupervised. It's a question generator with a human confirming every flag against the full QMS record — nothing more, and that's still useful.

The interesting result isn't "AI is great" or "AI hallucinates." It's that the failure was **legible and located**: high recall on real defects, a specific, reproducible over-reach on clean inputs. That's a property you can engineer against — and a far more useful answer than a single accuracy percentage.

---

*All examples reference synthetic data from a fictional, deliberately-unnamed pharmaceutical company, generated for research and educational purposes. No proprietary content from any current or prior employer is used or implied. This was a research experiment on generated data and a multi-agent harness — not a validated GxP system, and not advice for use on real investigations.*
