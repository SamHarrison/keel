# keel — requirements engineering for agentic software development

A template repository you clone at project inception. It carries a tailored
**ISO/IEC/IEEE 29148:2018** requirements process built for teams where LLM
agents write most of the code: four authored document layers, one CLI that
derives every analytical view, statement-level identity that survives
refactors, and three rings of deterministic gates that run identically in a
git hook, an agent's inner loop, and CI.

The agent-facing contract is **CLAUDE.md** (short rules + a documentation
map). This README is the human-facing explanation of the whole system.

## Quickstart

```sh
make init     # once per clone: .venv + deps + Ring 1 hooks + ledger/
make check    # the full local gate — green means CI will be green
```

Then run the day-one interview (`docs/elicitation/playbooks/inception.md` —
an agent conducts it against the founder), mint your first identities, and
cut the first baseline (`tools/req baseline cut inception`).

Ring 3 (GitHub Actions, `.github/workflows/gates.yml`) needs no setup.
Ring 2 (the `no-mistakes` push gate) is an opt-in accelerator: install
no-mistakes per-machine and the committed `.no-mistakes.yaml` wires keel's
commands in. A clone can never install tooling on your machine — by design.

## Why this exists

Requirements docs for agent-built software fail in known ways, and every
mechanism in keel answers one of them:

- **Docs drift from code** → everything derivable is *derived* by `req`
  and byte-verified; hand-editing a derived file fails the gate.
- **References rot silently.** In the ancestor project, renumbering broke
  41 of 264 references — each still *resolved*, to the wrong row. → identity
  is permanent and random (never positional), references pin versions, and
  stale pins are hard errors with a mechanical fix.
- **Status columns lie** → status is computed from evidence (tests citing
  rows), never stored in a field that can go stale.
- **Vague language ships** → a denylist + shall-grammar lint, at error
  severity on the rows you touched, warning severity on legacy debt.
- **Executive fiat becomes untraceable lore** → every business requirement
  carries a stakeholder and a `source:` pointing at an elicitation record.

## Concepts

**Identity.** Every statement has one permanent 25-bit identity with three
interchangeable forms: alias (`alpine-pixel` — docs and prose), Crockford
token (`15NM7` — commits, issue titles, test names), canonical integer
(tooling). `req mint` draws them randomly (collisions retried against the
registry); they are never hand-invented, never reused, never renamed.
`req resolve X` converts any form. Prose lines in vision/scenarios are
citable via end-of-line anchors `[#TOKEN]`.

**Versions and pins.** Statement text is hashed into `ledger/versions.lock`.
Any normative-text change bumps the version mechanically (`req version`) and
every inbound pinned reference `[[alias@N]]` is rewritten in the same pass —
docs, links, and test names alike. A pin that disagrees with the lock is a
hard error; the lock itself is audited against the git diff in CI, so it
cannot be quietly rewritten.

**File kinds.** *Authored* (docs/ — ID'd, reviewed), *derived* (build/ —
regenerated, never committed), *ledger* (ledger/ — machine-written memory
like versions.lock: committed, never hand-edited, diff-audited).

**Layers** (`docs/`): `vision.md` (strategy, ≤200 lines) → `profiles/`
(stakeholder classes: customers `CP-n` and internal `IP-n`) → `brd/`
(outcome-shaped business requirements — the only layer with priority; every
row has a stakeholder and a source) → `scenarios/` (operational narratives)
→ `prd/` (the obligations: typed, witnessed shall-statements,
customer-agnostic) → `trace/links.yaml` (authored m:n join) →
`architecture.md` + `decisions/` (ADRs) + `reviews/`.

**Unknowns.** A question becomes a `tbd:` block ({question, owner, opened,
trigger}) — never a prose hedge. A *doubted reference* becomes
`[[HOLE "phrase" was:OLD-ID]]`, which fails every gate until judged through
`req migrate` (worksheet → two blind passes → agreement applies,
disagreement escalates). A *product-level absence* is an ADR scope-out with
a reopen condition. Baselines force triage of all three.

**Witnesses and the RTM.** Each PRD row declares how it will be verified:
`test | demo | analysis | inspection | none` (none = honestly not provable
by automation). Tests claim rows by citation in the test name
(`alias@version #method`); code claims with `keel:implements` comments.
`req rtm` derives the bidirectional matrix and a three-valued verdict per
row — witnessed / unwitnessed (with the reason) / not-provable-by-test — and
a row is only witnessed by its own method (one unit example can't prove a
universal).

**Gates — three rings, one verdict set.** Ring 1: pre-commit hook + `make
check` (seconds, local). Ring 2: no-mistakes push gate (optional; findings
that would alter normative text park as ask-user, mechanical ones auto-fix).
Ring 3: GitHub Actions — the unskippable floor. All three run the same `req`
commands; passing locally *is* passing.

**Plans, ADRs, spec edits — three different artifacts.** A plan is
prescriptive steps for an epic (ephemeral — deleted when the epic closes).
An ADR is a fork taken, with rationale (permanent —
`decisions/YYYYMMDD_HHMMSS_slug.md`, never renamed). A spec edit changes a
guarantee. Most value-picks are spec edits with no ADR; a scope-out is an
ADR with no spec edit. Execution lives in GitHub Issues citing aliases;
authored docs never cite issue numbers back.

## Worked example: an internal business constraint

The CPO says: *"Use package X — building experience with it is a key
business objective, above customer requirements."* Where does that go?

1. The CPO is a **stakeholder** (29148 §5.2.2): they live in an internal
   profile, `docs/profiles/IP-1.yaml` (`kind: internal`).
2. The objective is a **BRD row**: outcome-shaped ("the team has production
   experience with X"), `stakeholder:` the CPO's alias, `priority:` ranked,
   `acceptance:` an observable demo, `source:` the elicitation record of
   that conversation. "Above customer requirements" = the profile's `rank`.
3. It flows through `links.yaml` to a **PRD row `type: constraint`** — "The
   system shall implement <capability> using package X", `witness:
   inspection`. Implementation detail is legal here because the mechanism
   *is* the requirement (29148 §5.2.5).
4. The fork itself (X over alternatives, what was accepted) is an **ADR**
   whose `traces:` cite both rows; `architecture.md` lists X in the stack.

If X conflicts with a customer requirement, that tension is an authored
`conflicts` link — visible in the trace, not resident in someone's head.

## Command reference (`tools/req`)

| Command | What it does |
|---|---|
| `mint` | Draw a fresh identity (canonical ≡ alias ≡ token). Never by hand. |
| `resolve X` | Convert/locate any identity form. |
| `lint` | Strict schemas, identity/projection, wordlist pins, quality lints (error on changed rows, warn corpus-wide), lock drift. |
| `xref` | Dangling refs, stale pins, open HOLEs, `section:` targets, malformed `[[…]]`. |
| `version` | Reconcile the lock: bump changed statements, cascade every inbound pin. `--check` = drift gate · `--audit` = diff-anchored ledger audit (CI). |
| `render` | Readable views of the row layers → `build/render/`. `--verify` = byte-identity. |
| `trace` | Registry, INDEX, TBx register → `build/`. |
| `slice EXPR` | Minimal context bundle for one identity (agents read this, not the tree). |
| `rtm` | Bidirectional matrix + witnessed/unwitnessed verdicts, gaps, orphans, stale. |
| `measure` | Volatility, TBx age, witness debt (29148 §6.6.3). |
| `migrate audit/merge/apply` | The HOLE workflow: worksheet → double-blind judgement merge → deterministic re-attachment. |
| `baseline cut NAME` | Forces triage (open TBx, due triggers, untriaged warnings) then tags. |
| `init` | Bootstrap a fresh clone (used by `make init`). |

## Life cycle (the loops)

L0 bootstrap (`make init` → inception interview → first baseline) →
L1 discovery (elicit → record → normalize → BRD rows) → L2 definition (PRD +
links against the gap report) → L3 build (issues/epics cite aliases; ADRs
for forks) → L4 verification & validation (witness burn-down; validation =
acceptance demos to the named stakeholder) → L5 baseline & change (tags,
register triage, trend measures).

## Standards stance

Tailored conformance to ISO/IEC/IEEE 29148:2018 per its §4.5 and Annex C —
clause dispositions and tailoring circumstances in `docs/process.md` §9.
The four layers realize BRS/StRS/SyRS/SRS content; derived views are
information items per §7 ("information items do not require physical
documentation" when the content lives organized in a repository).

## Gotchas

- Template placeholder rows (`word-word`, id 0) are lint-exempt until you
  mint real identities — gates begin to bite from your first real row.
- `.venv/` is the toolchain: `make` targets prefer it automatically; bare
  `python3 tools/req` fails unless deps are global.
- arxivhaiku is pinned by commit SHA (bootstrap + gates.yml) and
  cross-guarded by wordlist digests in `keel.yaml`: bump one, re-verify the
  other, or lint fails — that is the point.
- The alias separator is per-project (`keel.yaml: alias_separator`).

Status: v0.4 consolidation build — decision log K-1…K-22 settled
(design record: the keel integrated plan + consolidation plan, kept with
the project owner).
