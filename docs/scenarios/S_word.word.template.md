---
# TEMPLATE (copy-and-edit, never edit in place; delete or keep for
# reference). Copy to S_<alias>.md after `req mint`. The actor MUST be a
# stakeholder row from a profile — the triple below is lint-verified.
uid: "00000"
alias: word.word
version: 1
slug: <short-descriptor>
mode: normal            # normal | degraded | adverse
stakeholder_uid: "00000"
stakeholder_alias: word.word
stakeholder_name: <actor role, e.g. lab operations manager>
---
# <title> — a <mode> day for <actor>

<Narrate minute-by-minute, in the actor's voice, ≤120 lines. At each beat
ask "what must be true here?" — every answer is a candidate BRD or PRD row.
Anchor only load-bearing beats with [#TOKEN] (mint real tokens). Wire the
scenario to the PRD rows it exercises in trace/links.yaml
(`from: <this alias>`); rows discovered here cite this file as `source:`.>

## Worked example of a GOOD scenario (delete when you copy)

> **08:40** — Dana (lab operations manager) scans the low-stock report over
> coffee. Three reagents are below threshold; one is flagged *supplier
> discontinued*. She needs the flag to be impossible to miss. [#XXXXX]
>
> **08:52** — She opens the discontinued reagent and sees every experiment
> that consumed it in the last 90 days, with owners. She messages the two
> heaviest users: "alternatives by Friday?" — the system must answer *who
> depends on this*, not just *how many are left*. [#XXXXX]
>
> **09:15** — Reorder for the other two: she approves the pre-filled
> purchase draft without retyping quantities (last order + usage trend).
> One click, audit-logged against her account. [#XXXXX]
>
> **11:30** — A grad student asks why their order is delayed. Dana pastes a
> link to the order's status page instead of forwarding emails. The link
> will still work next month. [#XXXXX]
>
> **What must be true (harvested into rows):** discontinued flags surface
> unprompted · consumption is queryable by artifact and time window ·
> reorder drafts derive from history · every approval is attributed ·
> status links are permanent references.
>
> Why this example is good: one named actor (a real stakeholder) · concrete
> times and artifacts, no generalities · each beat ends in a testable "must
> be true" · the degraded/adverse variants ("supplier API is down", "a
> student tries to approve their own order") become sibling scenarios with
> mode: degraded / adverse, not buried paragraphs here.
