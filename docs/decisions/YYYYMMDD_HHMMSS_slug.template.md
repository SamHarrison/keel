---
# TEMPLATE (copy-and-edit): copy to YYYYMMDD_HHMMSS_slug.md — the filename
# IS the permanent ID: real timestamp, never renamed, never deleted. Batch
# review rulings share ONE rulings ADR.
status: proposed        # proposed | accepted | rejected | deprecated | superseded-by:<filename-id>
date: "0000-00-00"      # decision date (or last status change), ISO 8601
decision-makers: []
consulted: []           # two-way input (people/agents whose views were sought)
informed: []            # one-way notification
traces: []              # aliases/anchors this decision touches — xref-gated
# tbd: {question: ..., owner: ..., opened: 0000-00-00, trigger: ...}
---
# <short title: problem + solution>

## Context and Problem Statement
<forces at play, citing rows as `[[alias]]` (floating) or `[[alias@n]]` (pinned)>

## Decision Drivers
* <driver>

## Considered Options
* <option 1>
* <option 2>

## Decision Outcome
Chosen option: "<option>", because <justification>.

### Consequences
* Good, because <…>
* Bad, because <…>

### Confirmation
<How the ruling lands: cite changed rows as `[[alias@n]]`. For a scope-out,
state "the spec is deliberately silent; this ADR is the only record" AND give
the reopen condition. Merging an ADR touches architecture.md or carries the
arch-unchanged label (docs/process.md §10).>

## Pros and Cons of the Options
<optional — delete freely>

## More Information
<supersedes/related links, review finding IDs, non-normative issue context>
