# process & reference — THE ONE NORMATIVE DOCUMENT (v0.5).
# §§1–10 are the core; §§11–18 the full reference;
# docs/process/architecture-layer.md and docs/process/rtm.md are normative
# modules by inclusion. schema/*.json and tools/req IMPLEMENT this spec:
# where implementation and this document disagree, the document is right
# and the implementation has a bug — file a `spec-gap` issue (the same
# code-vs-spec doctrine the PRD applies to product code). The top-level
# README.md belongs to the project; humans enter there, agents via
# CLAUDE.md.

## 1 · Principles
P1 The unit of truth is the addressable statement (identity: §2).
P2 Three file kinds: authored (ID'd, reviewed); derived (build/, rebuilt
   byte-for-byte by `req trace`/`req render`; never hand-edited; never
   committed); ledger (ledger/, machine-written memory the tree cannot
   rebuild — versions.lock, migration-map — committed, never hand-edited,
   and diff-audited: every ledger delta must be entailed by an authored-text
   delta in the same change (`req version --audit`, Rings 2–3).
P3 Context is scarce: layer budgets; read build/INDEX.md then slices, not trees.
P4 Gates are deterministic and habitat-identical (hook = agent loop = CI).
P5 Execution in GitHub Issues/Projects; truth in the repo; references point
   one way (issues cite aliases; docs never cite issues).
P6 Elicitation has artifacts: playbooks, transcripts, normalization logs,
   `source:` provenance on BRD rows.
P7 Process is enforced culture: what can be mechanized is a gate; what cannot
   is an MR checklist applied to changed rows.

## 2 · Identity (arxivhaiku-backed)
One identity, three forms: uid = Crockford token (`15NM7`, the display
form) ≡ alias (`alpine.pixel`) ≡ canonical 25-bit integer (tooling only)
; bijection per arxivhaiku (wordlist SHA-256s
pinned in req.yaml and gate-checked; deprecation-overlay immutability).
`version` is the process's own, integer, bumped mechanically on any normative-text
change: `req version` reconciles against ledger/versions.lock (16-hex hash
of pin-normalized text — re-pinning is not a change, so the pin cascade
terminates in one pass) and rewrites every inbound pin. References: alias
(floating) or `alias@n` / `[[alias@n]]` (pinned; stale = hard error, cascade
mechanical); `[[HOLE "phrase" was:X]]` marks a reference awaiting judgement
and fails every gate until `req migrate` resolves it.
Prose lines are cited by end-of-line anchors `[#TOKEN]`; anchor density lint
warns above ~1/8 lines. Minting: `req mint` = haiku() → registry check →
retry; never by hand; canonicals never reused (the versions.lock ledger
remembers retired identities forever — `req mint` checks it).
Separator per-project (`alias_separator`); default dot (`word.word`).

## 3 · Layers (budgets in parentheses)
README.md ← BRS: the ROOT document — vision lives in it (≤200 lines,
≤20 anchors; humans enter here, agents via CLAUDE.md/AGENTS.md) ·
profiles/*.yaml (≤150) ←
StRS-context; the profile itself is a minted identity (uid/alias/version; no ordinal —
rank orders, alias identifies; filename CP_<alias>.yaml / IP_<alias>.yaml,
its BRD BRD-CP_<alias>.yaml with meta.profile = the alias, lint-enforced);
stakeholders 1:N, ID'd constraints; kind: customer
(ICP-ranked) | internal ( — the business is a stakeholder per 29148
§5.2.2; a strategic constraint enters as its BRD row, flows to a PRD
type: constraint row, and outranks customer work via profile rank only) ·
brd/*.yaml (≤40 rows) ←
StRS-req: outcome-shaped, stakeholder-tied (stakeholder_uid/alias/name,
all three for in-place readability; uid↔alias lint-verified), dual-ranked —
priority lives here only, split priority_stakeholder (the named holder's
urgency) vs priority_buying (the buying unit's rank)
· scenarios/*.md (≤120) ← OpsCon incl. degraded/adverse days · prd/*.yaml
(≤400 rows/section-file) ← SyRS+SRS merged: customer-agnostic shall-statements,
typed (functional|interface|quality|constraint|process|definition), witnessed
(test|demo|analysis|inspection|none) · trace/links.yaml ← authored m:n
(brd/scenario → prd aliases or section:NAME; satisfies|partial|informs|
conflicts) · decisions/YYYYMMDD_HHMMSS_slug.md (ADRs — see §10) ·
architecture.md — see process/architecture-layer.md (≤200 lines, truth
hierarchy, tripwires, ADR-coupling rule, baseline affirmation).

## 4 · TBx & register
Any authored row/ADR may carry tbd: {question, owner, opened, trigger, ref?}
with disposition open|deferred|out-of-scope (out-of-scope needs a reopen
condition). The register is derived; baselines force triage: every date
trigger overdue and every event trigger re-affirmed/resolved/killed before
the tag lands.

## 5 · Gates (three rings, one verdict set)
Ring 1: .githooks/pre-commit (staged lint+xref, <2 s) — also the agent inner
loop via `make check`. Ring 2: no-mistakes push gate (disposable worktree;
the repo's req commands wired into its lint/test/document steps; findings policy: any
finding altering normative text = ask-user, mechanical = auto-fix). Ring 3:
GitHub Actions gates.yml — the unskippable floor (branch protection), incl.
PR-body Trace: validation; no-mistakes ci-watch loops fixes for Ring-3 fails.
Gate list: strict schemas (unknown keys are errors) → id/version lint
(wordlist pins, alias projection, versions.lock drift) → xref (dangling,
stale pins, open HOLEs, section: targets) → quality lint (shall-grammar,
denylist, no priorities/profiles/vendors in PRD) → render --verify →
trace/RTM (ICP-P1 gaps block) → ledger audit (Rings 2–3). Quality severity
by scope: findings on rows changed in the diff are errors; corpus-wide
legacy findings warn, and baselines force their triage.

## 6 · RTM
Bidirectional, derived (build/rtm/): see process/rtm.md. Chain: stakeholder →
BRD → PRD → architecture (citations + ADR traces:) → code
(`// req:implements`) → tests (`// req:witnesses alias[@v]`). Views:
forward, reverse, gaps (down), orphans (up), stale, rtm.json — six derived
views, materialized from `req init` onward (blank-state before rows exist);
`req rtm impact ALIAS` prints a row's downstream closure for review scope.

## 7 · Loops
L0 bootstrap (init → inception interview → baseline/inception) · L1 discovery
(elicit→record→normalize→rows) · L2 definition (PRD+links against gaps) ·
L3 build (epics/issues cite aliases; ADRs; discoveries flow up) · L4 V&V
(witness burn-down; validation = BRD acceptance demos to the named
stakeholder) · L5 baseline & change (tags; register triage; measures:
volatility, TBx age, witness debt).

## 8 · Writing standard (MR checklist for changed rows)
necessary · singular · unambiguous · verifiable · implementation-free at its
layer · rationale where a value would puzzle · consistent with the set.
Write to survive adversarial misreading: bind every noun to a defined term;
one concept, one name; quantify or defer — never weasel, never fabricate;
close every set or state the generating rule; specify total behaviour
(absent/empty/min/max/one-past-max/malformed); exactly one row owns each
guarantee; never write a derived tally into authored text; prefer an honest
hole or tbd: to a confident falsehood. Requirements use 'shall' (ISO 29148
§5.2.7 warns against 'must'); prefer the positive form, and when negation IS
the guarantee bind it to the modal ("X shall not …"), never the subject
("no X shall …"). Rationale is timeless intent — never a claim about the
code or its history. Definitions are declarative rows (type: definition,
term:), never shall-statements. For every new or repointed reference, quote
to yourself the sentence in the target that states the guarantee — resolving
is not meaning (the 41-of-264 lesson).

## 9 · Standards stance
Tailored conformance to ISO/IEC/IEEE 29148:2018 per its §4.5 and Annex C;
the clause disposition table lives in the proposal (reference/) and is
normative here by inclusion. Tailoring circumstances (Annex C.2.3 a):
software products built with agentic coding workflows at solo-founder/small-
team scale; flat-text repository over an RE tool; information items realized
as the four layers plus derived views per §7's repository provision. RTM &
bidirectional traceability per §3.1.23–24, §6.4.3.5, §6.5.2. Rendered views
of row layers are derived information items: authored YAML is truth,
`req render --verify` gates byte-identity.

| 29148 information item | realization here |
|---|---|
| BRS (business) | README.md §Vision (+ business rows in BRDs) |
| StRS (stakeholder) | docs/profiles/ + docs/brd/ + docs/scenarios/ (OpsCon) |
| SyRS + SRS | docs/prd/ — the directory is the information item; section files are its volumes (§4.4 NOTE 2; §7; §7 NOTE 4 permit division, repository form, local titles) |
| RTM / VCRM (§6.5.2.2) | build/rtm/ — derived, never stored |
| Measures (§6.6.3) | build/measures.md |

## 10 · ADRs, reviews, plans (three artifacts)
A plan is prescriptive steps for an epic — ephemeral, deleted by the PR that
closes the epic (git retains it); never cited by ADRs or layers. An ADR is a
fork taken: docs/decisions/YYYYMMDD_HHMMSS_slug.md (real timestamp = the
permanent ID; never renamed), MADR-shaped with front-matter status/date/
decision-makers/consulted/informed + traces: (xref-gated) and tbd:.
Supersede = new ADR + flip the old status. Scope-outs live ONLY in ADRs
(the layers record no absence) and carry a reopen condition. A spec edit is
a guarantee change — most value-picks are spec edits with no ADR. Verified
code-vs-doc divergence becomes an issue labelled spec-gap citing the
falsified alias — never annotated into the layers. docs/reviews/ holds
permanent review evidence; declined findings get a written-rulings ADR so
no future review re-litigates them.

## 11 · Document flowdown

```
ENTRY — two doors, one root, and ONLY the root branches:

  agents ─→ CLAUDE.md (AGENTS.md / codex.md are shims) ─┐
  humans ─────────────────────────────────────────────── ┤
                                                         ▼
                                                     README.md

README.md IS the root: the project's face AND the vision (BRS) — the top
of the product spine lives in it. Two branches leave the root — humans and
agents alike reach both trees only through it:

PRODUCT (what the software must be — each layer answers the one above):
  README.md §Vision        the business problem, solution class, commitments
    → profiles/ (+ brd/)   who it serves; what they need, ranked, sourced
      → scenarios/         how a day with it actually goes
        → prd/             the obligations (the spec: typed, witnessed)
            ⇐ trace/links.yaml (authored join) ⇒
        → architecture.md + decisions/ (the how, and the forks taken)
          → code & tests   (cite rows: req:implements / alias@v in test names)

PROCESS (how work happens — each doc defers detail to the next):
  README.md §How this repo works (the summary)
    → CLAUDE.md            agent contract: must-follow rules + map
      → docs/process.md    THE NORMATIVE CORE (~130 lines)
        → docs/process/*   normative modules (architecture layer, RTM)
          → tools/req      the mechanization; --help on every command
```

Contents: [Quickstart](#quickstart) · [Why](#why-this-exists) ·
[Concepts](#concepts) · [Repository reference](#repository-reference-every-file) ·
[Schemas](#schema-reference-every-field) · [Command reference](#command-reference-toolsreq) ·
[Reference grammar](#reference-grammar) · [Gates](#gates--three-rings) ·
[Worked example](#worked-example-an-internal-business-constraint) ·
[Lifecycle](#life-cycle-the-loops) · [Standards mapping](#standards-mapping) ·
[Gotchas](#gotchas)

## 12 · Why this process exists

Requirements docs for agent-built software fail in known ways; every
mechanism here answers one of them:

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

## 13 · Repository reference (every file)

```
req.yaml                  project config: alias separator, wordlist pins
CLAUDE.md                 agent contract: rules + documentation map + project skeleton
README.md                 THE ROOT — project face AND vision (≤200 lines, ≤20 anchors)
AGENTS.md                 shim: points non-Claude agent harnesses at CLAUDE.md
Makefile                  init · check · trace · slice · baseline · hooks
.gitignore                ignores build/ (derived), .venv/, __pycache__/
.no-mistakes.yaml         Ring 2 wiring (inert until no-mistakes is installed per-machine)
.githooks/pre-commit      Ring 1: staged lint + xref, <2 s (armed by make init)
.github/workflows/gates.yml   Ring 3: full gate suite on every push/PR
.github/pull_request_template.md  Trace: line + changed-row checklist
.github/ISSUE_TEMPLATE/   epic.yml · spec-change.yml · tbx.yml
.github/CODEOWNERS        review routing
docs/profiles/CP_word.word.yaml   layer 2 — customer profile template (kind: customer)
docs/profiles/IP_word.word.yaml   layer 2 — internal profile template (kind: internal)
docs/brd/BRD-CP_word.word.yaml    layer 2 — business requirements template (priority lives here ONLY)
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
docs/process.md           THIS FILE — the one normative document (core §§1–10 + reference §§11–17)
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

## 14 · Schema reference (every field)

All schemas are **strict**: unknown keys are errors. Identity per row:
`uid` (5-char Crockford Base32 token, the canonical 25-bit integer's native
display form) + `alias` (`word.word`; separator per-project, default dot);
versions are integers ≥1, machine-managed. **Block style is mandatory in all
authored YAML** (one field per line): flow mappings `{…}` are rejected by
lint — commas inside braces silently create stray keys. Short flow
sequences (`refs: []`, `traces: []`) are fine.

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

**`docs/profiles/*.yaml`** (profiles.schema.json) — the profile is itself a
minted identity: `uid` + `alias` + `version` (no ordinal — `rank` orders,
the alias identifies) · **filename = `CP_<alias>.yaml` / `IP_<alias>.yaml`**
(prefix = kind) and the matching BRD is **`BRD-CP_<alias>.yaml`** /
**`BRD-IP_<alias>.yaml`**, its `meta.profile` holding the profile alias —
lint enforces all of it, so filenames can never go stale (no profile index
file for the same reason: an unversioned second source of truth) · `slug`
(human descriptor) · `kind` (**customer | internal**) · `rank` (portfolio order across
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

**`req.yaml`** — `alias_separator` (default `.` → `word.word`; changing
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

## 15 · Command reference (`tools/req`)

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
| `baseline cut NAME` | | Forces triage — open TBx, due `date:` triggers, untriaged corpus warnings all block — then tags `baseline/NAME`. |
| `init` | | Fresh-clone bootstrap: ledger/, hooks path (used by `make init`). |
| `sync` · `new` | | TODO — issue-sync helpers; need a live GitHub project. |

## 16 · Reference grammar

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
| `req:implements alias[@N]` in code | implementation claim (RTM forward trace) |

Anything else inside `[[…]]` is a malformed-reference error at load time.

## 17 · Worked example: an internal business constraint

The CPO says: *"Use package X — experience with it is a key business
objective, above customer requirements."*

1. The CPO is a **stakeholder** (29148 §5.2.2) → an internal profile
   (`IP_<alias>.yaml`, `kind: internal`), stakeholder row minted.
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

## 18 · Gotchas

- Template placeholder rows (`word-word`, id 0) are lint-exempt until you
  mint real identities — gates begin to bite from your first real row.
- `.venv/` is the toolchain; `make` targets prefer it automatically. Bare
  `python3 tools/req` fails unless deps are global.
- arxivhaiku is pinned by commit SHA (tools/bootstrap + gates.yml) and
  cross-guarded by the wordlist digests in req.yaml: bump either, re-verify
  the other, or lint fails — that is the point.
- The alias separator is per-project (`req.yaml`, default `.`); uids and
  anchor tokens are always uppercase Crockford 5-char.
- A clone never installs tooling on your machine: `make init` is the one
  deliberate act (and Ring 2's daemon is a separate per-machine install).


