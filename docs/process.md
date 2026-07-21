# keel process — normative (v0.4, consolidates proposal v1.0 + v1.1 + v1.2
# + the arkhive harvest per plan/keel_consolidation_plan.md, K-16…K-22)

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
pinned in keel.yaml and gate-checked; deprecation-overlay immutability).
`version` is keel's, integer, bumped mechanically on any normative-text
change: `req version` reconciles against ledger/versions.lock (16-hex hash
of pin-normalized text — re-pinning is not a change, so the pin cascade
terminates in one pass) and rewrites every inbound pin. References: alias
(floating) or `alias@n` / `[[alias@n]]` (pinned; stale = hard error, cascade
mechanical); `[[HOLE "phrase" was:X]]` marks a reference awaiting judgement
and fails every gate until `req migrate` resolves it.
Prose lines are cited by end-of-line anchors `[#TOKEN]`; anchor density lint
warns above ~1/8 lines. Minting: `req mint` = haiku() → registry check →
retry; never by hand; canonicals never reused (retired stays in registry).
Separator per-project (`alias_separator`); default dot (`word.word`).

## 3 · Layers (budgets in parentheses)
vision.md (≤200 lines, ≤20 anchors) ← BRS · profiles/*.yaml (≤150) ←
StRS-context; the profile itself is a minted identity (uid/alias/version;
filename <id>_<alias>.yaml, its BRD BRD-<id>_<alias>.yaml — lint-enforced);
stakeholders 1:N, ID'd constraints; kind: customer (CP-n,
ICP-ranked) | internal (IP-n — the business is a stakeholder per 29148
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
conflicts) · decisions/ADR-*.md (front-matter: status, traces:, tbd:) ·
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
keel commands wired into its lint/test/document steps; findings policy: any
finding altering normative text = ask-user, mechanical = auto-fix). Ring 3:
GitHub Actions gates.yml — the unskippable floor (branch protection), incl.
PR-body Trace: validation; no-mistakes ci-watch loops fixes for Ring-3 fails.
Gate list: strict schemas (unknown keys are errors) → id/version lint
(wordlist pins, alias projection, versions.lock drift) → xref (dangling,
stale pins, open HOLEs, section: targets) → quality lint (shall-grammar,
denylist, no priorities/profiles/vendors in PRD) → render --verify →
trace/RTM (ICP-P1 gaps block) → ledger audit (Rings 2–3). Quality severity
by scope: findings on rows changed in the diff are errors; corpus-wide
legacy findings warn, and baselines force their triage (K-19).

## 6 · RTM
Bidirectional, derived (build/rtm/): see process/rtm.md. Chain: stakeholder →
BRD → PRD → architecture (citations + ADR traces:) → code
(`// keel:implements`) → tests (`// keel:witnesses alias[@v]`). Views:
forward, reverse, gaps (down), orphans (up), stale; `req rtm impact ALIAS`
comments PRs with downstream closure.

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
of row layers are derived information items (K-22): authored YAML is truth,
`req render --verify` gates byte-identity.

## 10 · ADRs, reviews, plans (three artifacts)
A plan is prescriptive steps for an epic — ephemeral, deleted by the PR that
closes the epic (git retains it); never cited by ADRs or layers. An ADR is a
fork taken: docs/decisions/YYYYMMDD_HHMMSS_slug.md (real timestamp = the
permanent ID; never renamed), MADR-shaped with front-matter status/date/
decision-makers/consulted/informed + keel's traces: (xref-gated) and tbd:.
Supersede = new ADR + flip the old status. Scope-outs live ONLY in ADRs
(the layers record no absence) and carry a reopen condition. A spec edit is
a guarantee change — most value-picks are spec edits with no ADR. Verified
code-vs-doc divergence becomes an issue labelled spec-gap citing the
falsified alias — never annotated into the layers. docs/reviews/ holds
permanent review evidence; declined findings get a written-rulings ADR so
no future review re-litigates them.
