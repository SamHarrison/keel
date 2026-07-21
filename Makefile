check: ; ./tools/req lint && ./tools/req xref && ./tools/req render --verify && ./tools/req trace --gate
trace: ; ./tools/req trace
index: trace
slice: ; ./tools/req slice "$(Q)"
baseline: ; ./tools/req baseline cut "$(NAME)"
hooks: ; git config core.hooksPath .githooks
.PHONY: check trace index slice baseline hooks
