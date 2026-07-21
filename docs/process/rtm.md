# The Bidirectional RTM — `build/rtm/`

> keel process module. The Requirements Traceability Matrix is a **derived
> artifact** compiled from authored surfaces — never hand-maintained. This doc
> defines both.

## 1 · Standards grounding

ISO/IEC/IEEE 29148:2018 contains this by name: §3.1.23 defines requirements
traceability as the documented upward derivation path and downward
allocation/flow-down path (parent/child requirements); §3.1.24 defines the
**requirements traceability matrix** as the structured artifact linking
requirements to higher-level needs or lower-level implementation; RTM appears
in the standard's abbreviation list. §6.4.3.5 names **bi-directional
traceability** as a technique and enumerates what each requirement should trace
to: lower-level requirements, **the architecture**, **the system elements that
implement it**, **the verification/test entities that satisfy it**, and upward
to parent requirements and stakeholder needs — with requirements derived from
studies traceable back to those studies. §6.5.2 has verification results
documented in an RTM or VCRM. keel's full chain below is that list, made
concrete for a git repo.

## 2 · The chain and its authored surfaces

The RTM is compiled; the *links* are authored, each at the layer where the
judgment naturally lives:

| Link (both directions derived) | Authored surface | Who writes it |
|---|---|---|
| Stakeholder need ↔ BRD row | `stakeholder:` + `source:` fields on BRD rows | product, during elicitation |
| Vision anchor ↔ BRD row | `anchors:` field on BRD rows (optional) | product |
| BRD row / scenario ↔ PRD rows | `trace/links.yaml` | eng lead |
| PRD row ↔ architecture | alias citations in `architecture.md` drivers/invariants + `traces:` in ADR front-matter | eng lead |
| PRD row ↔ implementing code | `// keel:implements alias[, alias]` annotation at file or symbol level (any language; regex-detected) | whoever writes the code |
| PRD row ↔ verifying test | `// keel:witnesses alias[@v][, …]` on the test (legacy bare `// witnesses:` accepted) | whoever writes the test |
| Derived requirement ↔ study | `source:` on the row pointing at the report/ADR; reports cite rows by `alias@version` | author of either |

Annotation rules: `keel:implements` claims *this element realizes that
obligation* — attach it at the smallest scope that honestly claims it (a file
header for a module-sized claim, a symbol comment for a function-sized one).
Do not blanket-annotate; an implements claim is a statement the RTM will hold
you to. Pinned `@v` on a witness means "verified against that wording"; a
version bump flips the claim to **stale — re-affirm**.

## 3 · Derived outputs (`req trace` → `build/rtm/`)

- `rtm.json` — the whole graph, machine-readable; everything else renders from it.
- `forward.md` — per BRD row: the full flow-down (need → PRD rows → modules/ADRs
  → code elements → tests), with per-level status glyphs.
- `reverse.md` — per PRD row: parents (BRD/scenario/anchor), architecture
  touchpoints, implementing elements, witnessing tests, citing reports.
- `gaps.md` — **downward holes**, per the standard's coverage analysis: BRD rows
  with no PRD support (blocks on ICP priority-1); PRD rows with no implementing
  element (warn until the owning epic exits, then block); witnessed-but-untested
  debt.
- `orphans.md` — **upward holes**, the compliance mirror: PRD rows no link
  justifies (gold-plating, quarterly review); code elements whose
  `keel:implements` targets don't resolve or whose claims nothing verifies;
  tests witnessing retired rows.
- `stale.md` — every `@v`-pinned claim whose target has advanced, with diffs.

## 4 · Impact analysis (the standard's third use, wired into the loop)

`req rtm impact ALIAS` prints the downstream closure of a row — every PRD child,
module, ADR, code element, and test that a change to it touches. Two habitats:

- **MR-time:** the Actions gate comments the impact set on any PR that edits an
  authored row, so review scope is computed, not guessed.
- **Ring 2:** in a no-mistakes run, the review step receives the impact set for
  changed rows as reviewer context.

## 5 · Gates summary (delta to `req trace --gate`)

| Check | Severity |
|---|---|
| ICP P1 BRD row with broken chain at any level down to PRD | **block** |
| PRD row unimplemented after its epic's exit baseline | **block at baseline** |
| Unresolvable `keel:implements` / `keel:witnesses` target | **block** |
| Stale pinned claims | warn (block at baseline until re-affirmed) |
| Orphans at any level | warn; quarterly triage |

The matrix itself is never edited, never committed, and carries no IDs — delete
`build/rtm/` and `req trace` recreates it byte-for-byte. That property, not
discipline, is why this RTM cannot rot the way hand-kept matrices famously do.
