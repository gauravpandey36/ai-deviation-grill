# Credits & Attribution

## Prior work this builds on

The conversational discipline of the **deviation-grill** skill — *one question at a time, walk
the decision tree depth-first, refuse to stop until every branch is resolved* — is adapted from
**Matt Pocock's `grill-me` skill**:

- **`grill-me` SKILL.md:** https://github.com/amazingloft999-droid/mattpocock-skills/blob/main/skills/productivity/grill-me/SKILL.md
- **Original author:** Matt Pocock
- **Upstream license:** MIT

Matt Pocock's `grill-me` is a general-purpose interrogator that relentlessly interviews you about
a plan or design until every branch of the decision tree is resolved, surfacing gaps and
misalignments before work begins.

## What is original here

This project **adapts that interrogation discipline to the pharmaceutical GxP deviation /
root-cause-analysis domain** and adds, as original work:

- five GxP guardrails (interrogate the investigation not the person; never assert facts; never
  accept "human error"/"retraining" as a terminal root cause; never let a CAPA pass without
  linkage + prevention + a measurable effectiveness check; convert the unanswerable to tracked
  open items);
- a depth-first tree mirroring a 7-step deviation investigation;
- a per-branch toolkit (5-Whys, Ishikawa/6M, FMEA, Is/Is-Not, Reason's Swiss-cheese, Rasmussen
  SRK);
- a four-role controlled evaluation harness (Generator / Defendant / Grill / Judge) with hidden
  answer keys; and
- a single-pass audit mode for structured deviation records.

With gratitude to Matt Pocock for the original `grill-me` pattern.

---

_All examples reference a fictional pharmaceutical company built for
research and educational purposes. No proprietary content from any current or prior employer is
used or implied._
