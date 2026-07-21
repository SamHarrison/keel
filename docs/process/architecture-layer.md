# The Architecture Layer — `docs/architecture.md`

> keel process module. Merge into `process.md` §3 or keep standalone; either way
> this is the normative definition of the architecture file. Template:
> `docs/templates/architecture.md`.

## 1 · What it is, and the truth hierarchy

The architecture file is the **map, not the territory**. It records the shape of
the system — modules, boundaries, data ownership, and the things deliberately
absent — at a level of detail chosen to stay true for months, not days.

The truth hierarchy it lives inside, stated once so "the codebase is the
ultimate truth" means exactly what it should:

| Question | Authority |
|---|---|
| What is the product *obligated* to do? | The PRD. Code that disagrees is defective, not authoritative. |
| What does the system *actually* do, and how? | **The codebase and its tests.** Always. |
| Why is it shaped this way? | ADRs (decisions, dated) + this file (the current consolidated shape). |
| Where do I look? | This file. Its job is navigation and intent, nothing more. |

The architecture file therefore never *duplicates* what code can say for itself
(signatures, schemas, sequences, class structure). It says only what code
*cannot* self-narrate: why a module exists, what may depend on what, which
invariants are load-bearing, and what was considered and rejected.

## 2 · Format and hard budget

- Markdown, **≤200 lines** (linted — over budget fails `req lint`). Concision is
  a feature: a file short enough to re-read in five minutes gets re-read; one
  that isn't, rots.
- Detail ceiling: context + containers/modules (C4 levels 1–2). Anything finer
  belongs in code, tests, or an ADR.
- Section skeleton (see template):
  1. **Purpose** — ≤5 lines; cites the vision anchors it serves.
  2. **Drivers** — the ranked forces, each citing BRD/PRD aliases.
  3. **Context** — one diagram (ASCII or mermaid): the system and its neighbors.
  4. **Module table** — name · responsibility · owns-data · may-depend-on ·
     authoritative code path. One row per top-level module.
  5. **Invariants** — the load-bearing rules, each as an anchored line
     (`[#15NM7]`) so PRD rows, ADRs, and tests can cite them.
  6. **Deliberately absent** — what the architecture refuses to contain, so its
     absence reads as a decision rather than an omission.
  7. **ADR index** — one line per area: which ADRs shaped it.

## 3 · Staleness countermeasures (the point of this doc)

Documentation overhang is prevented structurally, not aspirationally:

1. **The budget** (above). Small documents stay true longer and cost minutes to
   verify.
2. **Mechanized tripwires in `req lint`** — the checks that CAN be automated,
   are: every module-table row's `code path` must exist; module names must
   cover the top-level source directories (a new `src/` dir with no module row,
   or a row pointing at nothing, fails); every cited alias/anchor must resolve;
   every ADR listed must exist, and every non-superseded ADR must appear in the
   index.
3. **The ADR coupling rule** — an MR that merges a new or superseding ADR must
   either touch `architecture.md` or carry the label `arch-unchanged` with one
   line of justification. Decisions are exactly the moments maps drift; this
   pins the map to them.
4. **Baseline affirmation** — `req baseline cut` includes an architecture step:
   re-read the file (it's ≤200 lines), then affirm or fix. The affirmation is
   recorded in the baseline tag message. A map affirmed at every baseline is
   never more than one baseline stale.
5. **The detail ceiling** — the content most prone to staleness (sequence
   detail, schemas, class relationships) is *banned from the file*, so the file
   cannot rot along its most rot-prone axis.

What is deliberately NOT mechanized: whether the prose *meaning* still matches
the code's shape. That is the baseline-affirmation reader's job, kept honest by
the budget. A tripwire that pretended to check semantic drift would be worse
than none.

## 4 · Relationships

- **PRD → architecture:** drivers and invariants cite the PRD rows they answer;
  the RTM's architecture link set is derived from these citations plus ADR
  `traces:` front-matter (see `rtm.md`).
- **Architecture → code:** the module table's code paths are the RTM's bridge
  from shape to implementation, and the lint tripwire keeps them live.
- **ADRs:** record *changes* of shape with their reasoning, immutably; this
  file consolidates the *current* shape. Reading order for a newcomer: this
  file, then the ADRs its index points at, then code.
