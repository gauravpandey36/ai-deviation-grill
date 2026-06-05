"""Seeded deviation archetypes for the Phase-1 controlled evaluation (see the experiment design).

Each archetype defines the KIND of investigation to generate and the KIND of defects to
plant. The Generator turns these into a full case: a `grill_input` (the flawed deviation
record the Grill sees), a `case_packet` (the fuller truth the Defendant role-plays from),
and an `answer_key` (the planted defects the Judge scores recall against). The answer key
is stored separately and NEVER shown to the Grill.
"""

ARCHETYPES = [
    {
        "key": "human_error_masking_system",
        "title": "Human-error root cause masking a system cause",
        "guidance": (
            "An operator made an error, and the investigation stops at 'operator did not "
            "follow SOP' / 'retraining'. The TRUE systemic cause (plant in case_packet, "
            "OMIT from grill_input) is a latent condition: e.g. the SOP step is ambiguous, "
            "two steps are easily transposed, the step is unworkable at line speed, or the "
            "operator was trained on a superseded revision. Plant defects: terminal "
            "human-error root cause; retraining-only CAPA; no preventive/forcing-function; "
            "no effectiveness check."),
    },
    {
        "key": "equipment_calibration",
        "title": "Equipment / calibration excursion",
        "guidance": (
            "A measurement or process excursion traces to an instrument out of calibration "
            "or overdue PM. Plant defects: investigation never checks the calibration "
            "history / audit trail; scope to other batches measured on the same instrument "
            "between the last good cal and discovery is missing; CAPA fixes the one "
            "instrument but no preventive program-level action (cal interval review)."),
    },
    {
        "key": "material_supplier",
        "title": "Material / supplier-attributed cause",
        "guidance": (
            "Cause attributed to incoming material or a supplier component. Plant defects: "
            "no CoA / incoming-inspection check cited; supplier change-notification history "
            "not reviewed; scope to other lots using the same material lot omitted; CAPA "
            "blames the supplier with no internal detectability improvement."),
    },
    {
        "key": "procedure_ambiguity",
        "title": "Procedure ambiguity",
        "guidance": (
            "The SOP/protocol is genuinely ambiguous or internally contradictory. Plant "
            "defects: investigation treats it as a one-off slip rather than a procedure "
            "defect; no check of how many other operators interpreted the step differently; "
            "CAPA is 'reminded the operator' rather than fixing the procedure text."),
    },
    {
        "key": "data_integrity_alcoa",
        "title": "Data-integrity / ALCOA+ concern",
        "guidance": (
            "A data-integrity flavor: a result reprocessed without audit-trail review, a "
            "shared login, a missing original record, an out-of-spec result not carried "
            "into the average. Plant defects: audit trail not reviewed; ALCOA+ attributes "
            "(Attributable, Original, Contemporaneous) not addressed; CAPA is procedural "
            "with no system control (access, audit-trail review SOP)."),
    },
    {
        "key": "planted_conflict",
        "title": "Investigation with a planted speaker CONFLICT",
        "guidance": (
            "Two contributors give CONTRADICTORY accounts of a key fact (e.g. QA says the "
            "line cleared at 14:00, the operator says cleaning ran until 15:30; or two "
            "different root causes are asserted). The grill_input must contain BOTH "
            "conflicting statements, unresolved. Plant defects: the conflict itself "
            "(unresolved contradiction); investigation picked one side with no evidence to "
            "adjudicate; downstream impact/CAPA built on the unverified side."),
    },
    {
        "key": "thin_but_clean",
        "title": "Thin but genuinely clean",
        "guidance": (
            "A SHORT but legitimately sound investigation: a minor deviation with a correct, "
            "evidence-backed systemic root cause, a linked CAPA with a real preventive "
            "element and a measurable, time-bound effectiveness check. Plant ZERO defects. "
            "answer_key.planted_defects MUST be an empty list. This is the false-positive / "
            "noise control: a good Grill should surface few or no gaps and should NOT "
            "manufacture problems."),
    },
]

CASE_SCHEMA_DESCRIPTION = """
Return ONE JSON object, and nothing else, with EXACTLY these top-level keys:

{
  "case_id": "DEV-EVAL-<archetype_key>",
  "archetype": "<archetype_key>",
  "title": "<short deviation title>",
  "grill_input": {
     // The deviation record AS THE GRILL SEES IT — realistic synthetic data,
     // WITH the planted holes (missing fields left absent or vague; conflicting statements
     // left unresolved). Use fields like: deviation_id, product, lot_number, process_step,
     // equipment_id, classification, description_what_happened,
     // description_what_should_have_happened, document_deviated_from, immediate_corrections,
     // investigation_steps, root_cause_category, root_cause_description, impact_assessment,
     // batch_disposition, capa (with id, description, and — IF the archetype plants a defect —
     // a missing/weak effectiveness_check), linked_change_control. For planted_conflict,
     // include a "statements" list with two contradictory attributed quotes.
  },
  "case_packet": {
     // The FULLER TRUTH the Defendant role-plays from: everything in grill_input PLUS the
     // facts that WOULD resolve the planted holes if the Grill asks the right question
     // (the true systemic cause, the calibration history, the CoA result, how other
     // operators read the step, the audit trail, which conflicting statement the evidence
     // supports, etc.). The Defendant reveals these ONLY when directly and correctly asked,
     // and NEVER volunteers them.
  },
  "answer_key": {
     "planted_defects": [
        {
          "id": "D1",
          "branch": "problem_statement|containment|scope_impact|root_cause|capa|effectiveness|open_items|conflict",
          "type": "missing_evidence|human_error_terminal|retraining_only_capa|no_preventive_action|no_effectiveness_check|unresolved_conflict|scope_gap|alcoa_gap",
          "description": "<the specific hole a competent Grill should surface>",
          "ideal_grill_behavior": "<what a good Grill question/flag looks like for this defect>"
        }
        // ... (EMPTY LIST for thin_but_clean)
     ]
  }
}

Rules:
- 100% synthetic data (products GC-101/GC-201/GC-301; sites
  SITE-GC-01 Cambridge, CDMO-1 Pharmagen Dublin, CDMO-2 BioProcess Solutions Basel). No
  real company names.
- Make grill_input realistic and self-consistent EXCEPT for the deliberately planted holes.
- The planted defects must be genuinely diagnosable from the gap between grill_input and
  case_packet — not trick questions.
- Output ONLY the JSON object. No markdown fences, no commentary.
"""
