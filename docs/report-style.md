# Report Style Guide

> keel core module: `docs/report-style.md`. Governs every HTML/PDF report in
> the project. The companion boilerplate `docs/report-boilerplate.html`
> carries the canonical CSS and one exemplar of every component — clone it, fill
> it, delete what a given report doesn't need. Agents: treat this file as
> normative when producing any report; treat the boilerplate's CSS as frozen
> tokens.

## 0 · The three governing habits

1. **Verdict first.** The cover ends in a callout stating the conclusion; the
   executive summary is 3–5 findings, not a tour of the sections. A reader who
   stops after page one leaves correctly informed.
2. **Provenance pinned.** Every report freezes its inputs on the cover: commit
   hashes, document versions, dates, companion artifacts. Reports are records;
   a report whose inputs can drift is an opinion with page numbers.
3. **Color is meaning.** Every color in the palette has one semantic job,
   identical across all reports. Nothing is colored for decoration.

## 1 · Design tokens (frozen — change only by amending the template)

**Type.** DejaVu Sans throughout (ships with weasyprint; renders identically in
HTML and PDF); DejaVu Sans Mono for identifiers, aliases, paths, code. Base
9.6pt / line-height 1.45, body justified. Scale: H1 22–23pt (tight
letter-spacing −0.5pt) · H2 13–13.5pt · H3 10.8–11pt · H4 9.8pt · small/captions
8–8.2pt · figure fine print never below 7pt.

**Palette.**

| Token | Hex | Meaning (everywhere, always) |
|---|---|---|
| ink | `#22303c` | body text |
| navy | `#184a7b` | structure & authority: H2 rules, table headers, primary systems in diagrams, info callouts |
| steel | `#2f6b8f` | secondary systems/modules |
| slate | `#4a5a66` / `#5b6770` | subtitles, captions, secondary annotations |
| muted | `#8a97a0` | meta labels, colophon, parked/skipped |
| hairline | `#ccd5db` / `#d7dee4` | table row rules, pre borders |
| green | `#2f8f4e` | pass · adopt · allocated · recommended |
| amber | `#e6a817` | caution · partial · medium · needs-ruling |
| orange | `#d96a1e` | high severity · degraded fit |
| red | `#c43d3d` | blocker · risk · rejected · gap |
| blue | `#3a6fb0` | informational · operational class |
| purple | `#6b4fb3` | meta-work: investigation prompts, candidate-B, open trades |

The severity ramp (green→amber→orange→red) differs in *lightness*, not just
hue, so it survives grayscale printing. Do not introduce new colors; a new
semantic need reuses the ramp or earns a template amendment.

## 2 · Page architecture (A4 / PDF)

- `@page` A4; margins **22mm top · 18mm sides · 20mm bottom** — enough air to
  hold the page without covering text, with clearance for running furniture.
- Running furniture: classification top-right ("CONFIDENTIAL — Engineering
  Design"); document identity bottom-left ("project · report name vX");
  "Page N of M" bottom-right — all 7.5pt muted. The **cover suppresses all
  three** (`page: cover`).
- Page budgets: decision memo 6–10 pp · phase report 15–25 pp · anything past
  ~36 pp should have been two documents.
- `page-break-after: avoid` on all headings; `page-break-inside: avoid` on
  table rows, callouts, and figures — a split callout or orphaned heading is a
  QA failure.

## 3 · Cover anatomy (top to bottom)

1. **Eyebrow** — 8pt, +2.2pt letterspacing, navy, uppercase: the document
   class ("INITIAL DESIGN REPORT · SOFTWARE ARCHITECTURE").
2. **H1** — the product/project name, large and tight.
3. **Subtitle** — one sentence, slate: what this report does, not what it is.
4. **Accent rule** — 2.4pt navy, ~34mm wide. The only decorative element.
5. **Meta table** — label column in 7.8pt uppercase muted; rows for:
   commission (what was asked), inputs with **pins** (commit/sha/version),
   builds-on (companion artifacts), status, prepared date.
6. **Verdict callout** — the conclusion, in the callout class matching its
   temper (ok/warn/risk). Non-negotiable: no cover without a verdict.

## 4 · Structure & navigation

- TOC on its own page using CSS `target-counter` so page numbers resolve in
  PDF; entries are the H2 list plus appendices — no deeper.
- H2s numbered `N · Title` with the navy bottom border; H3 `N.n`; H4 for
  finding/trade items, usually opening with a badge.
- Appendices carry **verbatim artifacts** (embedded files, full listings) in
  `pre` blocks — spliced in whole and HTML-escaped, never retyped.
- Close with the colophon line: em-dash, report identity, date, input pins,
  companions — 8.2pt muted.

## 5 · Typography & prose discipline

- Every identifier — alias, path, command, config key, version — sits in a
  mono chip (`code`/`.mono`: mono font on `#f0f3f6`). No exceptions; the chips
  are how a skimmer finds the load-bearing nouns.
- Bold opens a point (`**Decision:** …`, `**Rationale:** …`) — never
  mid-sentence emphasis spray. Italics for terms of art and one-word stresses.
- Tables speak in fragments; prose speaks in sentences. Don't mix registers
  within a cell.
- Findings and trades are **numbered with stable IDs** (S-1, CA-1, RT-3, OT-2,
  K-11, R-4…) so later documents can cite them; once published, an ID is never
  renumbered.

## 6 · White space

The report breathes through fixed rhythm, not ad-hoc gaps: 6pt after
paragraphs; 17–18pt above H2 / 11–12pt above H3; 6–10pt around tables; 7–8pt
around callouts and figures. Two rules of thumb: **no wall pages** — every
page should carry at least one structural element (heading, table, callout,
figure) breaking the prose; and **never add space by empty elements** — if the
rhythm feels wrong, the content is (usually a section that wants splitting).

## 7 · Trades & comparisons (the heart of these reports)

**7.1 Choose the right instrument.**

| You are showing… | Use |
|---|---|
| Which option and why (qualitative) | Comparison table: option-per-column, criterion-per-row, verdict phrasing per row ("Advantage: A, moderate") |
| How much, defensibly (quantitative) | Weighted scorecard: weights sum to 100, scores 0–10, per-row one-line basis, totals row |
| A settled decision | RT pattern: badge + `**Options** · **Decision** · **Rationale** · **Consequences**` as labeled inline runs |
| An unsettled decision | OT pattern: `**Question** · **Options** · **Criteria** · **Leaning**` + an investigation-prompt block |
| Many items' status at a glance | Disposition badges in a table column, or a colored strip/heat figure |

**7.2 Scorecard obligations.** A score without a stated basis is an opinion —
every criterion row carries its one-line justification. Totals within ±0.5 are
ties and must be called ties. **Sensitivity analysis is mandatory**: show the
one weight that decides, rezero it, restate the totals ("remove dimension 1
and the race is a coin-flip"). The scorecard's job is to make disagreement
precise, not to end it — say so when true.

**7.3 Verdicts never live inside tables.** The table carries evidence; the
verdict gets a callout adjacent to it. A reader scanning callouts alone should
reconstruct every conclusion in the document.

**7.4 Badge vocabulary** (frozen): severity `BLOCKER/HIGH/MEDIUM/LOW/ADVISORY`
(red/orange/amber/blue/muted) · disposition `ADOPT/ADAPT/SKIP` and
`RECOMMENDED/PARKED/REJECTED` (green/amber/muted-red) · trade class `RT-n`
(navy) / `OT-n` (purple) · change class `CHANGE REQUEST/COST DRIVER/RULING
NEEDED`. Badges are 7.2pt bold white on the semantic color, 2.5pt radius.

**7.5 Fairness furniture.** Comparative reports state their fairness rules in
§method (symmetric adversarial passes, refined-vs-refined, spec-as-yardstick)
and carry corrections visibly — a superseded claim is restated in a warn
callout, never silently edited.

## 8 · Diagrams & figures

- **Inline SVG by default**: self-contained, version-controllable, crisp at
  any zoom, and weasyprint renders it natively. Raster (base64 PNG) only for
  data-dense generated graphics (heat maps), at ≥150dpi effective.
- Canvas convention: width 660px (≈172mm inside margins); font DejaVu Sans,
  8.2–9.5pt in-figure, ≥7pt floor; node palette per §1 (navy = primary system,
  steel = secondary, plain stroke = external/store, green fill = decisive
  strength/target, red fill = wound/gap, dashed = optional/degraded path).
- Every figure: numbered, referenced from body text, and captioned with **the
  takeaway, not the description** — "Green saturation is the point: the
  exceptions cluster exactly where the open trades live," not "Coverage heat
  map."
- Comparison diagrams use the two-column card layout (one bordered card per
  candidate, strengths/wounds bands at the bottom).
- Label edges; unlabeled arrows are decoration. A deliberately-absent list
  beside an architecture figure ("no message bus, no cache tier — and why")
  earns its keep more often than another box does.
- ASCII diagrams are fine in markdown sources; reports render SVG.

## 9 · Callouts

Four classes, one job each: `.callout` (navy: framing, method, the cover
verdict when neutral) · `.ok` (green: recommendation, clean verdict) · `.warn`
(amber: caveat, correction, honest limit) · `.risk` (red: blocker, required
ruling). One bold lead phrase, then prose. Density: about one per page —
callouts are the skim layer, and a page of callouts has no skim layer.

## 10 · Content patterns proven in this project

- **Numbered-findings exec summary** with severity badges, each finding one
  bullet: claim → evidence chips → consequence.
- **"What is deliberately absent/omitted"** section in every design: absences
  as decisions, each with its reason and reinstatement tripwire.
- **Investigation prompts** (purple block, `INVESTIGATION PROMPT · OT-n`
  label): every open question ships with a ready-to-run brief including
  acceptance criteria — a report that leaves work should leave it executable.
- **Registers over prose hedges**: open items as TBx-style tables (item ·
  disposition · owner · trigger), never scattered "we should eventually…".
- **References section** for research-based reports; alias@version citations
  for internal documents.

## 11 · Build & QA pipeline

1. Author HTML from the template; embed verbatim artifacts via `__TOKEN__`
   placeholders spliced with an HTML-escaping script (never paste-escape by
   hand).
2. Render: `weasyprint report.html report.pdf` (or the two-line Python).
3. **Structural QA before delivery** (non-optional): page count sane for the
   budget; grep the extracted text for every section marker, figure caption,
   and key ID; confirm no `__TOKEN__` survived; confirm TOC page numbers
   resolved. Know the harmless failures: pypdf extraction inserts spaces and
   splits hyphenated words — verify by locating the substring before declaring
   a real miss.
4. Deliver HTML **and** PDF together; the HTML is the source of record (this
   project has already once needed the HTML recovered after a PDF-only
   delivery).

## 12 · Accessibility & print

Grayscale-check any new figure (the ramp survives; two same-lightness hues
side-by-side don't). Minimum contrast: slate on white is the floor for
meaningful text; muted is furniture only. Never encode meaning in color alone
in tables — pair the badge word with the color, which the badge vocabulary
already guarantees.
