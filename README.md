# keel — requirements-engineering scaffold for agentic software development

Clone this at project inception. It gives you: four authored document layers
(vision → profiles+BRDs → scenarios → PRD), an authored trace join, a
bidirectional RTM and every analytical view derived by one CLI (`tools/req`),
statement-level identity via arxivhaiku, three gate rings (pre-commit /
no-mistakes push gate / GitHub Actions), and elicitation playbooks an agent
runs against the founder on day one.

Quickstart: `./tools/req init` · then run docs/elicitation/playbooks/inception.md
· then `tools/req baseline cut inception`.

Normative process: docs/process.md. Agent contract: CLAUDE.md.
Status: v0.3 skeleton — see HANDOFF packet plan §5 for per-file build state.
Standards stance: tailored conformance to ISO/IEC/IEEE 29148:2018 (§4.5),
declared in docs/process.md appendix.
