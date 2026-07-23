# Research — decision-supporting evidence

Research reports, standards analyses, and study results that a decision
rests on live here, under the same never-delete contract as ADRs and
reviews (they are cited; deletion breaks the provenance chain). The ADR
that consumed the research cites it from its Confirmation or More
Information section; the research file links back to that ADR once it
exists.

Distinct from docs/reviews/ (review evidence about *this project's
artifacts*) and from plans (ephemeral). Short findings that need no
standalone file are folded directly into the ADR body instead.

Naming: `YYYYMMDD_HHMMSS_<slug>.md` — real timestamps, ISO 8601 (same
convention as ADRs, reviews, and elicitation records).

Research reports delivered as HTML/PDF follow docs/report-style.md
(cloning docs/report-boilerplate.html); markdown research archives are
exempt. HTML is the source of record; PDFs regenerable, gitignored.
