CLEAVE ?= $(if $(wildcard ../cleave/target/release/cleave),../cleave/target/release/cleave,cleave)
YARA_PRECOMPILE ?= $(or $(wildcard ../cleave/target/release/yara-precompile),$(wildcard $(dir $(CLEAVE))../cleave/target/release/yara-precompile),$(wildcard /var/lib/cyclotron/cleave/target/release/yara-precompile),$(shell command -v yara-precompile 2>/dev/null),yara-precompile)
# Prefer the installed CLI; fall back to a sibling cleave checkout's build.
# `go run github.com/atomdrift-project/cleave/tools/yara-update@latest` does not
# work today: that directory declares `module yara-update`, so the import path
# the repo layout implies isn't the module's own path.
YARA_UPDATE ?= $(if $(shell command -v yara-update 2>/dev/null),yara-update,$(abspath ../cleave/tools/yara-update/yara-update))

COMPILED_DIR := third-party/compiled

.PHONY: validate precompile yara-compile yara-update install-precommit

# Rule validation.
#
# Nothing here gates on third-party/compiled/. Those artifacts are built into a
# published bundle, not committed, and a stale or absent `.yrc` set is inert at
# runtime anyway -- the engine ignores it and compiles from source, so the
# failure mode is a slower client, not a wrong verdict.
validate:
	$(CLEAVE) --traits-dir . validate

# Compile the third-party + built-in YARA rules into portable per-filetype
# `.yrc` files (plus a manifest) under third-party/compiled/. These are BUILD
# ARTIFACTS, not repository content: a published bundle is assembled and served
# from R2, and that bundle is the only path by which precompiled rules reach a
# client. cleave then loads them with no in-process compilation. The `.yrc`
# hold WASM bytecode, so one build is loadable on every client architecture
# and OS.
#
# Generation runs against the STAGED tree, never the working tree. The manifest
# records a fingerprint of the rule sources it was built from, so an untracked
# stray `.yar`/`.yaml` in a working copy would bake in a fingerprint no clean
# checkout can reproduce — and the engine would then reject the very files we
# shipped, silently falling back to compiling from source on every client.
# Output goes to a fresh directory and replaces third-party/compiled/ wholesale
# rather than being written over it: an in-place write would leave behind any
# bucket the current rules no longer produce (a filetype that lost its last
# rule, or one renamed by an engine fix) and ship it forever.
precompile:
	@tmp=$$(mktemp -d) && trap 'rm -rf "$$tmp"' EXIT && \
	  mkdir -p "$$tmp/src" && git checkout-index -a --prefix="$$tmp/src/" && \
	  CLEAVE_TRAITS_DIR="$$tmp/src" $(YARA_PRECOMPILE) "$$tmp/out" && \
	  rm -rf $(COMPILED_DIR) && mkdir -p $(COMPILED_DIR) && \
	  cp -R "$$tmp"/out/. $(COMPILED_DIR)/ && \
	  echo "Compiled YARA rules -> $(COMPILED_DIR)/ (from the staged tree)"

# Fetch the latest third-party rule sources, then re-compile so the `.yrc` in a
# bundle built from this tree match the rules they were built from.
yara-update:
	cd third-party && "$(YARA_UPDATE)"
	$(MAKE) precompile

# Prior name, kept so existing scripts and muscle memory keep working.
yara-compile: precompile

install-precommit:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	@echo "Pre-commit hook installed."
