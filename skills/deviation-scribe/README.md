# deviation-scribe (placeholder)

The Scribe is the upstream extractor (transcript → tagged fields + gap list) that the Grill
chains from. It was **intentionally skipped** for this experiment: per the experiment design: the
real records (`investigation_data/particle_deviations.json`) are **structured deviation
records, not meeting transcripts**, so they are ingested directly by the Grill — no Scribe
needed. Drop the Scribe prompt here and wire Scribe→Grill only if/when transcript inputs are added.

_Research/educational note. Synthetic the fictional company data only._
