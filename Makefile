REQ := $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3) tools/req

init: ; ./tools/bootstrap
check: ; $(REQ) lint && $(REQ) xref && $(REQ) version --check && $(REQ) render --verify && $(REQ) trace --gate
trace: ; $(REQ) trace
index: trace
slice: ; $(REQ) slice "$(Q)"
baseline: ; $(REQ) baseline cut "$(NAME)"
hooks: ; git config core.hooksPath .githooks
.PHONY: init check trace index slice baseline hooks
