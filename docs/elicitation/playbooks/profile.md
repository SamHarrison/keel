# Profile deep-dive — run once per new customer profile (~30 min)

Run this when a new customer class appears (or when inception left a
profile thin). The asking and recording rules of `inception.md` apply
verbatim: questions in order, follow up until you could write the rows
yourself, never fill silence, transcript recorded verbatim to
`records/YYYYMMDD_HHMMSS_profile_<slug>.md`, every interpretive leap one
`needs-confirmation` line in a sibling normalization log.

## The interview, phase by phase

**1 · Organization & environment (→ profile `context`, `persona`).**
Describe the organization this profile represents: size, structure, and
the environment the product would live in. Who are the people who would
touch it, and how technical are they?

**2 · Tooling, identity, and network posture (→ ID'd constraints).**
What does their stack look like — cloud, on-prem, source control, CI? How
do people authenticate (SSO provider, directory)? What does the network
allow: egress, inbound, third-party services? What security or compliance
posture shapes what software may enter?
*Listen for:* each hard fact becomes one ID'd constraint row.

**3 · Scale and cost ceilings (→ `context.scale`, constraints).**
How many users, now and at success? What data volumes? What would the
product be allowed to cost — in money, and in operator time?

**4 · The stakeholder map (→ stakeholder rows).**
Who owns the outcome? Who owns the money? Who feels the pain daily? Who
can veto? Name each role; note buying-unit membership in the `role` text.

**5 · Business requirements per stakeholder (→ BRD seed rows).**
For each stakeholder: what must become true for them, and what observable
change would prove it? Rank each row twice — the buying unit's priority
and the named stakeholder's own urgency.

**6 · Evaluation and installation (→ constraints).**
Walk me through how this organization evaluates and adopts software: who
runs the trial, against what bar, on what timeline, with how much of
whose time? What install path is acceptable?

**7 · Vetoes (→ `priority_buying: 1` rows or constraints).**
What would make this profile reject a product that otherwise works?

## Translate, then finish

Mint the profile identity and every row with `req mint`. Write
`CP_<alias>.yaml` (`kind: customer`; set `rank` relative to every existing
profile, and `status` — is this the ICP, secondary, or parked?) and
`BRD-CP_<alias>.yaml` with the stakeholder triple, both priorities, an
`acceptance`, and a `source:` on every row. Deferred questions become
`tbd:` blocks. Then: `req version` → `make check` green → hand back the
`needs-confirmation` list.
