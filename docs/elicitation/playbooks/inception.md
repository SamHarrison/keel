# Inception interview — day one, ~60–90 min of founder time

The interviewer is normally an agent; the founder answers. The interview
walks the document flowdown in order — customers → stakeholders → business
requirements → scenarios → ranking → buying → internal mandates → solution
→ scope — so answers land in the layer they belong to as they are spoken.

## How to ask

- Ask the questions below **in order, one phase at a time**. Within a
  phase, ask follow-ups until you could write the rows yourself; do not
  move on while a needed fact is missing — and never fill a silence with
  your own assumption. If the founder says "pause", stop cleanly: record
  where you stopped and which phases remain.
- Prefer concrete prompts over abstract ones: "walk me through", "paint me
  a picture", "give me an example from last month".
- When an answer covers a later phase early, accept it, note it, and skip
  the duplicate question later.

## How to record

- Everything the founder says goes **verbatim** (typos included) into
  `docs/elicitation/records/YYYYMMDD_HHMMSS_inception_transcript.md`,
  with your questions inline. The transcript is a record: never tidy it.
- Every interpretive leap you make — merging two groups into one profile,
  assigning an unstated priority, quantifying "small team" — becomes one
  line in `…_HHMMSS_inception_normalization.md`, flagged
  `needs-confirmation`. One leap, one line.
- Facts you did not interpret are listed in the normalization log under
  "recorded without interpretation".

## The interview, phase by phase

**1 · Customers (→ docs/profiles/, kind: customer).**
Who are the customers? Give me all the context about them: their
organization, size, environment and tooling, technical depth, network and
security posture, and anything that shapes how software reaches them.
*Listen for:* profile `context`/`persona` fields and ID'd constraints.

**2 · Pain (→ BRD statements, README §Vision problem).**
What are their pain points and problems today? What would remain broken if
no solution is ever found — and what are the impacts of not solving it?
*Listen for:* the problem paragraph of the vision, and the stakes.

**3 · Stakeholders (→ profile stakeholder rows).**
Who are the stakeholders inside the buying unit — who signs, who owns the
budget, who can veto? And who lives with the pain daily? Give me context
about each and about the broader organization around them.
*Listen for:* one stakeholder row per named role; note buying-unit
membership in the `role` text.

**4 · Business requirements, per stakeholder (→ BRD rows).**
For each stakeholder in turn: what would a solution have to make true for
them? Paint me a picture of how they experience the pain now and how the
solution helps them. What observable change would prove it helped?
*Listen for:* outcome-shaped statements (never "shall"), one per row, each
with an `acceptance` a demo could show.

**5 · Non-negotiables (→ priority_buying = 1 rows).**
What are the non-negotiables — what would make the buying unit reject a
product that otherwise works?
*Listen for:* rows where the product "can have zero features but must meet
this"; these get `priority_buying: 1`.

**6 · Priorities (→ the two priority fields, profile rank).**
How do the business requirements rank for the buying unit? And separately:
how urgent is each row for its *named stakeholder*? How does one
stakeholder's need compare against another's?
*Listen for:* `priority_buying` vs `priority_stakeholder` per row — they
are different questions; record both, and flag every value you assigned
rather than heard.

**7 · Scenarios (→ docs/scenarios/, three files minimum).**
Tell me about a good day using the solution, minute by minute. Now a bad
day — something degraded or hostile. And what is the key moment where the
product really shows its value?
*Listen for:* three scenarios — `mode: normal`, `mode: degraded` (or
`adverse`), and the earns-its-keep moment — each with a named stakeholder
as its actor.

**8 · ICP and buying (→ profile rank/status, context).**
Which customers are the most important to serve — who is the ICP? Walk me
through how the solution would be evaluated and bought: who runs the
evaluation, against what bar, over what timeline.
*Listen for:* `status: icp` on one profile, `rank` across all profiles,
and evaluation-path facts as profile constraints.

**9 · Internal stakeholders (→ IP profile + its BRD).**
Are there internal stakeholders — within the team building this — with
their own requirements? Strategic technology choices, capabilities the
business wants to build, platform mandates?
*Listen for:* an `IP_<alias>` profile whose BRD rows carry the mandates;
each will later flow to a PRD `type: constraint` row plus an ADR.

**10 · The solution (→ README §Vision, PRD seed rows).**
Tell me about the solution you envision. What kind of thing is it — and
what is it deliberately not? What must it do? What product requirements
can you already state?
*Listen for:* the solution-class paragraph and commitments of the vision;
concrete "must do" statements become seed PRD rows (typed, witnessed).

**11 · Out of scope (→ scope-out ADRs).**
What is out of scope? For each exclusion: what would have to change to
reopen it?
*Listen for:* one ADR per deliberate exclusion — the layers record no
absence, so the ADR is the only record, and it must carry the reopen
condition.

## How to translate answers into the tree

Work from the top of the flowdown to the bottom, minting every identity
with `req mint` (never by hand):

1. Draft **README §Vision** from phases 2 and 10: problem & stakes, what
   it is and is not, commitments (anchor only load-bearing lines).
2. Write **profiles** (phases 1, 3, 8, 9): `CP_<alias>.yaml` per customer
   class, `IP_<alias>.yaml` if internal mandates exist; stakeholders and
   constraints as identity rows; `rank` across all profiles; `status` on
   customer profiles only.
3. Write **BRD rows** (phases 4–6): one per outcome, the stakeholder
   triple, both priorities, an `acceptance`, and a `source:` pointing at
   the transcript. Every value you chose rather than heard is flagged in
   the normalization log.
4. Write **scenarios** (phase 7): `S_<alias>.md` × 3 with actor triples
   and modes; anchor the load-bearing beats.
5. Write **scope-out ADRs** (phase 11) with reopen conditions; seed **PRD
   rows** (phase 10) only for requirements the founder stated explicitly.
6. Open a `tbd:` block for every question the founder deferred; leave
   nothing as a prose hedge.
7. **Update the three entry documents** — after inception, no placeholder
   may remain at any door of the repository:
   - **README.md** — delete the Keel section at the top (everything
     down to and including the `DELETE ON INCEPTION` marker), then
     make the rest project-true: the title becomes the product's name,
     the opening paragraph describes the product and its owner, §Status
     states the phase and the `baseline/inception` tag, and §Getting
     started gains any project-specific setup.
   - **CLAUDE.md** — fill the `## What this is` paragraph (product, whom
     it serves, current phase, owner) so an agent's first screen is
     project-true.
   - **AGENTS.md** — confirm the shim still points correctly (CLAUDE.md,
     README.md) and add any project-specific agent entry notes.

## Outputs (the definition of done)

Transcript + normalization log (timestamped names) · README fully
project-true (title, opening paragraph, §Vision, §Status, §Getting
started) · CLAUDE.md `What this is` filled · AGENTS.md confirmed · every
customer profile, plus the IP profile if applicable · one BRD per profile,
every row sourced · at least three scenarios · scope-out ADRs · seed PRD
rows if any · then: `req version` → `make check` green →
`req baseline cut inception` → present the founder the
`needs-confirmation` list and any phases that remain unanswered.
