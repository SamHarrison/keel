# keel — requirements engineering for agentic software development

A template repository you clone at project inception. It carries a tailored
**ISO/IEC/IEEE 29148:2018** requirements process built for teams where LLM
agents write most of the code: four authored document layers, one CLI
(`tools/req`) that derives every analytical view, statement-level identity
that survives refactors, and three rings of deterministic gates that run
identically in a git hook, an agent's inner loop, and CI.

**This README is the complete documentation — every file, every schema,
every command.** The agent-facing contract is CLAUDE.md (short rules + a
map); the normative process is docs/process.md; everything is explained
here.

Contents: [Quickstart](#quickstart) · [Why](#why-this-exists) ·
[Concepts](#concepts) · [Repository reference](#repository-reference-every-file) ·
[Schemas](#schema-reference-every-field) · [Command reference](#command-reference-toolsreq) ·
[Reference grammar](#reference-grammar) · [Gates](#gates--three-rings) ·
[Worked example](#worked-example-an-internal-business-constraint) ·
[Lifecycle](#life-cycle-the-loops) · [Standards mapping](#standards-mapping) ·
[Gotchas](#gotchas)

## Quickstart

```sh
make init     # once per clone: .venv + deps + Ring 1 hooks + ledger/
make check    # the full local gate — green means CI will be green
```

Then run the day-one interview (`docs/elicitation/playbooks/inception.md` —
an agent conducts it against the founder), mint your first identities, and
cut the first baseline (`tools/req baseline cut inception`).

## Why this exists

Requirements docs for agent-built software fail in known ways; every keel
mechanism answers one of them:

- **Docs drift from code** → everything derivable is *derived* by `req` and
  byte-verified; hand-editing a derived file fails the gate.
- **References rot silently.** In the ancestor project, renumbering broke 41
  of 264 references — each still *resolved*, to the wrong row. → identity is
  permanent and random (never positional), references pin versions, stale
  pins are hard errors with a mechanical fix.
- **Status columns lie** → status is computed from evidence (tests citing
  rows), never stored in a field that can go stale.
- **Vague language ships** → denylist + shall-grammar lint: error severity
  on rows you touched, warning severity on legacy debt.
- **Executive fiat becomes untraceable lore** → every business requirement
  carries a stakeholder and a `source:` pointing at an elicitation record.

## Concepts

**Identity.** Every statement has one permanent 25-bit identity in three
interchangeable forms: uid = Crockford token (`15NM7` — the display form
in YAML rows, commits, issue titles, test names), alias (`alpine.pixel` —
docs and prose), canonical integer (tooling only).
`req mint` draws them randomly with a registry collision check; never
hand-invented, never reused, never renamed. `req resolve X` converts any
form. Prose lines in vision/scenarios are citable via end-of-line anchors
`[#TOKEN]`.

**Versions & pins.** Normative text is hashed into `ledger/versions.lock`.
`req version` bumps changed statements and rewrites every inbound pin
`[[alias@N]]` in the same pass (docs, links, test names). Stale pin = hard
error. The lock is diff-audited in CI: a hand-edit fails the build.

**File kinds.** *Authored* (docs/ — ID'd, reviewed) · *derived* (build/ —
regenerated, never committed) · *ledger* (ledger/ — machine-written memory:
committed, never hand-edited, diff-audited).

**Unknowns.** Open question → `tbd:` block ({question, owner, opened,
trigger}). Doubted reference → `[[HOLE "phrase" was:X]]` (fails every gate
until judged via `req migrate`). Product-level absence → ADR scope-out with
a reopen condition. Baselines force triage of all three.

**Witnesses & RTM.** Each PRD row declares its verification method
(`test|demo|analysis|inspection|none`). Tests claim rows by citation in the
test name (`alias@version #method`); code claims with `keel:implements`.
`req rtm` derives the matrix and a three-valued verdict — witnessed /
unwitnessed (with reason) / not-provable-by-test — and a row is only proven
by its own method.

**Three artifacts.** Plan = prescriptive steps for an epic (ephemeral,
deleted when the epic closes). ADR = a fork taken (permanent,
timestamp-named). Spec edit = a guarantee changed. Scope-outs live only in
ADRs; verified code-vs-doc divergence is a `spec-gap` issue, never an
annotation. Issues cite aliases; authored docs never cite issue numbers.

## Repository reference (every file)

```
keel.yaml                 project config: alias separator, wordlist pins
CLAUDE.md                 agent contract: rules + documentation map + project skeleton
README.md                 this file — the complete human documentation
Makefile                  init · check · trace · slice · baseline · hooks
.gitignore                ignores build/ (derived), .venv/, __pycache__/
.no-mistakes.yaml         Ring 2 wiring (inert until no-mistakes is installed per-machine)
.githooks/pre-commit      Ring 1: staged lint + xref, <2 s (armed by make init)
.github/workflows/gates.yml   Ring 3: full gate suite on every push/PR
.github/pull_request_template.md  Trace: line + changed-row checklist
.github/ISSUE_TEMPLATE/   epic.yml · spec-change.yml · tbx.yml
.github/CODEOWNERS        review routing
docs/vision.md            layer 1 — strategy prose (≤200 lines, ≤20 [#TOKEN] anchors)
docs/profiles/CP-1.yaml   layer 2 — customer profile template (kind: customer)
docs/profiles/IP-1.yaml   layer 2 — internal-stakeholder profile template (kind: internal)
docs/profiles/_index.yaml presentation-only profile listing (not schema-validated)
docs/brd/BRD-CP1.yaml     layer 2 — business requirements template (priority lives here ONLY)
docs/scenarios/S-001-normal-day.md  layer 3 — operational narrative template
docs/prd/example.yaml     layer 4 — PRD section template (rename at inception; `core.yaml`
                          recommended for your first real section; one file per section)
docs/trace/links.yaml     the authored m:n join: BRD → PRD rows / section:NAME
docs/architecture.md      (created at inception from docs/templates/architecture.md)
docs/templates/architecture.md   the ≤200-line architecture-map template
docs/decisions/00000000_000000_template.md   ADR template (copy → YYYYMMDD_HHMMSS_slug.md)
docs/reviews/README.md    permanent review evidence — contract + naming
docs/elicitation/playbooks/inception.md   day-one founder interview (start here)
docs/elicitation/playbooks/profile.md     per-profile deep-dive interview
docs/elicitation/playbooks/scenario.md    scenario elicitation interview
docs/process.md           THE NORMATIVE CORE (~130 lines, §1–§10)
docs/process/architecture-layer.md  normative module: truth hierarchy, tripwires
docs/process/rtm.md       normative module: RTM chain and views
schema/*.schema.json      strict schemas (see Schema reference below)
tools/req                 the CLI (see Command reference below)
tools/reqlib/refs.py      THE definition of the reference grammar
tools/reqlib/hashing.py   what "changed" means (pin-normalized 16-hex SHA-256)
tools/reqlib/schemas.py   strict-schema validation wiring
tools/reqlib/versioning.py  lock reconcile · pin cascade · drift · diff audit
tools/reqlib/quality.py   shall-grammar, denylist compilation, rationale lints
tools/denylist.yaml       vague-term categories (ISO §5.2.7) + exception syntax
tools/bootstrap           idempotent env setup (venv + pinned deps + req init)
ledger/versions.lock      {key: {version, hash}} — machine-written, committed, audited
ledger/migration-map.json (only if migrating) legacy-ID map; doubles as mint ledger
build/                    ALL derived, never committed: registry.json · INDEX.md ·
                          register.md · render/{prd,brd,profiles,links}.md ·
                          rtm/rtm.md · measures.md · slices/
```

## Schema reference (every field)

All schemas are **strict**: unknown keys are errors. Identity per row:
`uid` (5-char Crockford Base32 token, the canonical 25-bit integer's native
display form) + `alias` (`word.word`; separator per-project, default dot);
versions are integers ≥1, machine-managed. Stakeholder/constraint/
requirement rows are written in **block style** (one field per line) —
condensed flow mappings are banned: commas inside `{…}` silently create
stray keys (the strict schemas catch it; don't invite it).

**`docs/prd/*.yaml`** (schema/prd.schema.json) — top level: `section`
(kebab slug) + `requirements` (≤400). Per row:

| field | values | notes |
|---|---|---|
| `uid` `alias` `version` | identity triple | minted by `req mint`; version managed by `req version` |
| `type` | functional · interface · quality · constraint · process · definition | `constraint` = externally-imposed (incl. internal-stakeholder mandates) |
| `term` | string | required iff `type: definition`, forbidden otherwise |
| `text` | the shall-statement | the ONLY normative field; hashed for versioning |
| `witness` | test · demo · analysis · inspection · none | how the row will be verified (29148 §6.5.2) |
| `refs` | [alias or alias@N] | structured cross-references |
| `rationale` | string | timeless intent — never code claims, never a hidden guarantee |
| `tbd` | TBx block | see tbx schema |

**`docs/brd/*.yaml`** (brd.schema.json) — `meta: {profile, version}` +
`requirements` (≤40). Per row: identity triple + `statement`
(outcome-shaped, NOT shall-form) · `stakeholder_uid` + `stakeholder_alias`
+ `stakeholder_name` (all three, so a row reads in one place; lint verifies
the uid↔alias projection and that the alias names a real profile
stakeholder row) · `priority_stakeholder` (the named stakeholder's urgency)
+ `priority_buying` (the buying unit's rank) — both ints ≥1, 1 = highest;
priority exists ONLY in BRDs · `acceptance` (observable demo signal) ·
`source` (elicitation record path, `records/YYYYMMDD_HHMMSS_<slug>.md` —
required) · `rationale` · `anchors` · `tbd`.

**`docs/profiles/*.yaml`** (profiles.schema.json) — `id` (CP-n | IP-n) ·
`slug` · `kind` (**customer | internal**) · `rank` (portfolio order across
ALL profiles — how "above customer requirements" is expressed) · `status`
(icp | secondary | parked — customer kind only, required there, forbidden
for internal) · `persona {role, proficiency}` · `context {environment,
scale{users_min,users_max}}` · `stakeholders` [identity triple + `role`, block style] ·
`constraints` [identity triple + `text`, block style]. BRD rows attribute to stakeholder
aliases defined here.

**`docs/trace/links.yaml`** (links.schema.json) — `links` array; each:
`brd` (alias[@N]) · `spec` ([alias[@N] or section:slug], ≥1) · `relation`
(satisfies | partial | informs | **conflicts**) · `note`. Links carry no
IDs — they are endpoint-identified.

**`tbd:` blocks** (tbx.schema.json, embeddable in any row/ADR) —
`question` · `owner` · `opened` (YYYY-MM-DD) · `trigger` (event, or
`date:YYYY-MM-DD` which baselines enforce) · `disposition` (open | deferred
| out-of-scope) · `reopen` (required for out-of-scope) · `ref`.

**`keel.yaml`** — `alias_separator` (default `.` → `word.word`; changing
it mid-project rewrites every alias — a migration event, not a config
tweak) ·
`wordlists.{adjectives,nouns}_sha256` (pins; lint fails if the installed
arxivhaiku's lists differ — an upgrade cannot silently re-map aliases).

**ADR front-matter** (template in docs/decisions/) — `status` (proposed |
accepted | rejected | deprecated | superseded-by:<id>) · `date` ·
`decision-makers` · `consulted` · `informed` · `traces` (aliases touched —
xref-gated) · optional `tbd`. Body: MADR sections (Context, Drivers,
Options, Outcome, Consequences, **Confirmation** — cites changed rows;
scope-outs state the deliberate silence + reopen condition).

**`tools/denylist.yaml`** — categories (superlatives, subjective,
ambiguity, open_ended, comparatives, loopholes, totality, bindingness,
vendor_tokens) of banned terms per ISO §5.2.7. Entries are strings or
`{term, unless_preceded_by: [words]}` (so "at most 200 MB" passes while
bare "most" fails). `vendor_tokens` is per-project.

## Command reference (`tools/req`)

Run via `make` targets or `.venv/bin/python tools/req <cmd>`.

| command | flags | what it does |
|---|---|---|
| `mint` | `--separator` | Draw a fresh identity (prints `uid  alias  canonical`), collision-checked vs tree + ledger. Never mint by hand. |
| `resolve X` | | Convert/locate any identity form; prints all three + where it lives. |
| `lint` | `--strict-new`, `--staged` | Strict schemas · identity/projection/wordlist pins · quality lints (shall-grammar, denylist, rationale rules; **error on rows changed vs git base, warn corpus-wide**; `--strict-new` = all errors) · lock drift · anchor density · architecture budget. |
| `xref` | `--staged` | Dangling refs · stale pins · open HOLEs · unknown `section:` targets · malformed `[[…]]` (load error, never skipped). Scans rows, links, ADRs, reviews; code spans are exempt. |
| `version` | | Reconcile the lock: bump every changed statement +1, cascade all inbound pins (docs + links + test files), verify round-trip. |
| `version --check` | | Drift gate: tree ↔ lock disagreement fails (also inside `lint`). |
| `version --audit` | `--base REF` | Diff-anchored ledger audit (CI): every lock delta must match a text delta; entries never deleted; +1 steps only. Catches hand-edited locks. |
| `render` | `--verify` | Readable views of prd/brd/profiles/links → build/render/ with GENERATED banner; `--verify` = byte-identity (determinism + hand-edit detection). |
| `trace` | `--gate` | Rebuild build/: registry.json, INDEX.md, TBx register.md. |
| `slice EXPR` | | Minimal context bundle for one identity → build/slices/ (agents read slices, not trees). |
| `rtm` | `--results FILE`, `--gate` | Bidirectional matrix → build/rtm/: witnessed / unwitnessed(reason) / not-provable verdicts, link gaps, orphans, stale citations. `--gate` fails on orphans/stale. |
| `measure` | | Volatility · TBx age · witness debt → build/measures.md (29148 §6.6.3). |
| `migrate audit` | `--count` | Worksheet of open HOLEs: location, context window, legacy id, mechanical suggestion (an anchor to TEST, never an answer). |
| `migrate merge` | `--v1 --v2 --out --conflicts` | Double-blind merge of two judgement passes: agreement applies, disagreement → conflicts file for owner tiebreak. |
| `migrate apply F` | | Deterministic write-back: re-attach agreed holes as `[[alias@current]]` (right-to-left, shared site numbering with audit). |
| `baseline cut NAME` | | Forces triage — open TBx, due `date:` triggers, untriaged corpus warnings all block — then tags `keel/NAME`. |
| `init` | | Fresh-clone bootstrap: ledger/, hooks path (used by `make init`). |
| `sync` · `new` | | TODO — issue-sync helpers; need a live GitHub project. |

## Reference grammar

Defined once in `tools/reqlib/refs.py`; scanned in row text/rationale,
links targets, ADRs, reviews, and tests. Markdown code spans/fences are
exempt (examples, not citations).

| form | meaning |
|---|---|
| `[[alias]]` | floating — whatever the statement says now; never stale |
| `[[alias@N]]` | pinned — hard error when the target moves; cascade re-pins mechanically |
| `[[HOLE "phrase" was:OLD-ID]]` | judgement pending — fails every gate until `req migrate` resolves it |
| `alias@N` (bare) | pin in `refs:` lists, links targets, test names |
| `section:slug` | links.yaml target for a whole PRD section |
| `[#TOKEN]` | end-of-line anchor giving a prose line identity |
| `alias@N #method` in a test name | test claims to witness that row via that method |
| `keel:implements alias[@N]` in code | implementation claim (RTM forward trace) |

Anything else inside `[[…]]` is a malformed-reference error at load time.

## Gates — three rings

One verdict set, habitat-identical (P4): the hook, `make check`, and CI run
the same commands.

- **Ring 1** `.githooks/pre-commit` (staged lint + xref, <2 s) and
  `make check` (adds version --check, render+verify, trace --gate).
- **Ring 2** the no-mistakes push gate — optional per-machine accelerator;
  `.no-mistakes.yaml` wires keel commands into its lint/test steps. Findings
  that would alter normative text park as **ask-user**; mechanical findings
  auto-fix. Never merges.
- **Ring 3** `.github/workflows/gates.yml` — the unskippable floor: pinned
  deps → lint --strict-new → xref → version --check → **version --audit**
  (ledger vs diff) → render determinism → trace → rtm.

Severity by scope: quality findings on rows changed in your diff are
errors; identical findings on untouched legacy rows warn — and `baseline`
refuses to tag until warnings are triaged. New debt can't enter; old debt
can't hide.

## Worked example: an internal business constraint

The CPO says: *"Use package X — experience with it is a key business
objective, above customer requirements."*

1. The CPO is a **stakeholder** (29148 §5.2.2) → internal profile
   `docs/profiles/IP-1.yaml` (`kind: internal`), stakeholder row minted.
2. The objective is a **BRD row**: outcome-shaped statement,
   `stakeholder_uid/alias/name` = the CPO, both priorities ranked, `acceptance:` an
   observable demo, `source:` the elicitation record of that conversation.
   "Above customer requirements" = the internal profile's `rank`.
3. `links.yaml` joins it to a **PRD row `type: constraint`** — "The system
   shall implement <capability> using package X", `witness: inspection`.
   Implementation detail is legal here because the mechanism *is* the
   requirement (§5.2.5).
4. The fork (X over alternatives) is an **ADR** with `traces:` citing both
   rows; `architecture.md` lists X. A conflict with a customer requirement
   is an authored `conflicts` link — in the trace, not in someone's head.

## Life cycle (the loops)

L0 bootstrap (`make init` → inception interview → `baseline cut inception`)
→ L1 discovery (elicit → transcript → normalization log → BRD rows with
`source:`) → L2 definition (PRD + links against the RTM gap report) → L3
build (epics/issues cite aliases; ADRs for forks; discoveries flow up) →
L4 V&V (witness burn-down; validation = acceptance demos to the named
stakeholder) → L5 baseline & change (tags; register triage; volatility /
TBx-age / witness-debt trends).

## Standards mapping

Tailored conformance to ISO/IEC/IEEE 29148:2018 per §4.5 + Annex C;
dispositions and tailoring circumstances in docs/process.md §9.

| 29148 information item | keel realization |
|---|---|
| BRS (business) | docs/vision.md (+ business rows in BRDs) |
| StRS (stakeholder) | docs/profiles/ + docs/brd/ + docs/scenarios/ (OpsCon) |
| SyRS + SRS | **docs/prd/** — the directory is the information item; section files are its volumes (§4.4 NOTE 2 permits division; §7 permits repository form; §7 NOTE 4 permits local titles) |
| RTM / VCRM (§6.5.2.2) | build/rtm/ — derived, never stored |
| Measures (§6.6.3) | build/measures.md |

## Gotchas

- Template placeholder rows (`word-word`, id 0) are lint-exempt until you
  mint real identities — gates begin to bite from your first real row.
- `.venv/` is the toolchain; `make` targets prefer it automatically. Bare
  `python3 tools/req` fails unless deps are global.
- arxivhaiku is pinned by commit SHA (tools/bootstrap + gates.yml) and
  cross-guarded by the wordlist digests in keel.yaml: bump either, re-verify
  the other, or lint fails — that is the point.
- The alias separator is per-project (`keel.yaml`, default `.`); uids and
  anchor tokens are always uppercase Crockford 5-char.
- A clone never installs tooling on your machine: `make init` is the one
  deliberate act (and Ring 2's daemon is a separate per-machine install).

Status: v0.4 consolidation build — decision log K-1…K-22 settled (design
record: the keel integrated plan + consolidation plan, kept with the
project owner).
