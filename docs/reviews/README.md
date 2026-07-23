# Reviews — permanent evidence

Review reports, ruling registers, and acceptance records live here under the
same never-delete contract as ADRs (they are cited; deletion breaks the
provenance chain). Distinct from plans, which are ephemeral and die with
their epic.

Declined or deferred review findings get a **written-rulings ADR** in
docs/decisions/ so no future review re-litigates them; an external review is
handed the full set: the layer files + docs/decisions/ + docs/process.md.

Naming: `YYYYMMDD_HHMMSS_<slug>.md` — real timestamps, ISO 8601 (same
convention as ADRs and elicitation records).

Reports filed here follow docs/report-style.md (verdict-first cover,
pinned inputs, frozen CSS tokens from docs/report-boilerplate.html);
HTML is the source of record, PDFs are regenerable and gitignored.
