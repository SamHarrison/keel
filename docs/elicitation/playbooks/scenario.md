# Scenario walkthrough — elicitation by narration (~20 min per scenario)

Run this to turn a stakeholder's real day into rows. One sitting produces
one scenario; a product needs at least three (`mode: normal`, `degraded`,
`adverse`). The asking and recording rules of `inception.md` apply: record
the narration verbatim to `records/YYYYMMDD_HHMMSS_scenario_<slug>.md`,
and log every interpretive leap as `needs-confirmation`.

## Setup (before asking anything)

Pick the **actor** — they must already exist as a stakeholder row in a
profile; if they do not, run the profile deep-dive first. Pick the
**mode**: a normal day, a degraded day (something the product depends on
is down or slow), or an adverse day (someone hostile, careless, or
overreaching).

## The walkthrough

Ask the actor's narrator (usually the founder) to tell the day **minute
by minute, in the actor's voice**, starting before the product is even
touched: "It's 8:40, coffee in hand — what happens first?" Keep the
narration concrete: real artifacts, real names for things, real times.

At every beat, ask the one question that matters: **"what must be true
here for this moment to go well?"** Write the answer down as stated, and
do not classify it mid-narration — keep the story moving. When the
narrator generalizes ("it should just be fast"), push once for the
observable version ("how long would they actually wait?").

When the day ends, read the harvested list back and ask: which of these
would the actor's organization actually pay for, and which merely annoy?

## Translate, then finish

1. Mint the scenario identity and write `S_<alias>.md` with its
   front-matter: `mode`, `slug`, and the actor's
   `stakeholder_uid/alias/name` triple — lint verifies the triple and the
   `S_<alias>.md` filename.
2. Keep the narration ≤120 lines, in the actor's voice; anchor only the
   load-bearing beats with `[#TOKEN]` (mint the tokens too).
3. Sort the harvested answers: outcome-shaped facts become BRD rows
   (sourced to this record); product obligations stated explicitly become
   PRD rows; everything uncertain becomes a `tbd:` block. Never leave a
   "must be true" as a prose hedge inside the scenario.
4. Once PRD rows exist for this scenario, add links
   (`from: <scenario alias>` → the rows it exercises) so RTM scenario
   coverage can see it; a scenario that exercises nothing appears in
   `build/rtm/gaps.md` until then.
5. Then: `req version` → `make check` green → hand back the
   `needs-confirmation` list and the gap notes.
