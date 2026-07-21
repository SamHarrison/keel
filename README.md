# keel — requirements-engineering scaffold for agentic software development

Clone this at project inception. It gives you: four authored document layers
(vision → profiles+BRDs → scenarios → PRD), an authored trace join, a
bidirectional RTM and every analytical view derived by one CLI (`tools/req`),
statement-level identity via arxivhaiku, three gate rings (pre-commit /
no-mistakes push gate / GitHub Actions), and elicitation playbooks an agent
runs against the founder on day one.

Quickstart (fresh clone): **`make init`** — creates .venv, installs deps
(pyyaml, jsonschema, arxivhaiku), arms the Ring 1 hooks, creates ledger/.
Then run docs/elicitation/playbooks/inception.md · then
`tools/req baseline cut inception`. Smoke: `make check`.

Ring 3 (Actions) needs nothing: gates.yml runs on every push/PR. Ring 2
(the no-mistakes push gate) is an opt-in accelerator: install no-mistakes
per-machine, add the remote, and `.no-mistakes.yaml` (committed here) wires
keel's commands in — a clone can never install it for you, by design.

Normative process: docs/process.md. Agent contract: CLAUDE.md.
Status: v0.4 consolidation build — decisions K-1…K-22 settled.
Standards stance: tailored conformance to ISO/IEC/IEEE 29148:2018 (§4.5),
declared in docs/process.md appendix.
