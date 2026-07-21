# Architecture — <product>
<!-- template · budget ≤200 lines · detail ceiling: context + modules -->
<!-- Truth hierarchy: PRD = obligations · code = implementation · this file = the map -->

## Purpose
<!-- ≤5 lines. What shape this system takes and why, citing vision anchors. -->
A <kind-of-system> serving <who>, shaped primarily by <dominant force>.
Serves: [#XXXXX] [#XXXXX]

## Drivers (ranked)
<!-- The forces that shaped the design, strongest first, each citing rows. -->
1. <driver> — per `alias-one`, `alias-two`
2. <driver> — per `alias-three`

## Context
```
[ actor ] ──> [ THIS SYSTEM ] ──> [ neighbor system ]
                     │
                     v
              [ data store ]
```

## Modules
<!-- One row per top-level module. `code` paths are lint-checked to exist and
     to cover the top-level source dirs. -->
| module | responsibility | owns data | may depend on | code |
|---|---|---|---|---|
| <name> | <one line> | <tables/buckets or —> | <modules or —> | `src/<dir>/` |

## Invariants
<!-- Load-bearing rules, one per line, each anchored so rows/ADRs/tests cite it. -->
- <invariant that must survive every refactor> [#XXXXX]
- <another> [#XXXXX]

## Deliberately absent
<!-- Absences that are decisions. One line each, with the ADR that decided it. -->
- No <thing>: <why> (<YYYYMMDD_HHMMSS_slug>)

## ADR index
<!-- One line per area; every non-superseded ADR appears somewhere here. -->
- <area>: <YYYYMMDD_HHMMSS_slug>, <YYYYMMDD_HHMMSS_slug>
