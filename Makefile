CLEAVE ?= $(if $(wildcard ../cleave/target/release/cleave),../cleave/target/release/cleave,cleave)
YARA_PRECOMPILE ?= $(or $(wildcard ../cleave/target/release/yara-precompile),$(wildcard $(dir $(CLEAVE))../cleave/target/release/yara-precompile),$(wildcard /var/lib/cyclotron/cleave/target/release/yara-precompile),$(shell command -v yara-precompile 2>/dev/null),yara-precompile)
# Prefer the installed CLI; fall back to a sibling cleave checkout's build.
# `go run github.com/atomdrift-project/cleave/tools/yara-update@latest` does not
# work today: that directory declares `module yara-update`, so the import path
# the repo layout implies isn't the module's own path.
YARA_UPDATE ?= $(if $(shell command -v yara-update 2>/dev/null),yara-update,$(abspath ../cleave/tools/yara-update/yara-update))

COMPILED_DIR := third-party/compiled

.PHONY: validate check-precompile precompile yara-compile verify-precompile yara-verify yara-update install-precommit

# Rule validation.
#
# This no longer gates on third-party/compiled/. The precompile targets below
# still work and are still the way to refresh those artifacts, but a stale or
# unfingerprinted `.yrc` set is not a reason to fail an ordinary trait edit:
# stale `.yrc` are inert at runtime (the engine ignores them and compiles from
# source), so the failure mode is a slower client, not a wrong verdict. Run
# `make precompile` (or `make verify-precompile`) deliberately when you are
# preparing a bundle to publish.
validate:
	$(CLEAVE) --traits-dir . validate

# Cheap correctness gate on third-party/compiled/: complete, fingerprinted, and
# built from the rule sources being committed. No compilation — one walk that
# hashes the rule text. Only rule sources count toward that fingerprint (`.yar`
# plus the trait YAML carrying an inline `type: yara` rule), so an ordinary
# trait edit does not send you back here.
#
# Sources come from the STAGED tree and the artifacts from the working tree,
# the same pairing `precompile` writes, so regenerating always clears this
# check immediately. Reading sources from the working tree instead would make
# untracked or gitignored `.yar` files (which never reach a client) count
# toward the fingerprint, and the check could then never be satisfied.
check-precompile:
	@tmp=$$(mktemp -d); trap 'rm -rf "$$tmp"' EXIT; \
	  git checkout-index -a --prefix="$$tmp/"; \
	  if CLEAVE_TRAITS_DIR="$$tmp" $(YARA_PRECOMPILE) --check $(CURDIR)/$(COMPILED_DIR); then :; else \
	    echo "  -> run 'make precompile', then 'git add $(COMPILED_DIR)'"; exit 1; fi

# Compile the third-party + built-in YARA rules into portable per-filetype
# `.yrc` files (plus a manifest) under third-party/compiled/. These are
# COMMITTED: a published bundle is a plain `git archive` of this repo, so
# precompiled rules only reach clients if they live in git. cleave then loads
# them with no in-process compilation. The `.yrc` hold WASM bytecode, so one
# build is loadable on every client architecture and OS.
#
# Generation runs against the STAGED tree, never the working tree. The manifest
# records a fingerprint of the rule sources it was built from, so an untracked
# stray `.yar`/`.yaml` in a working copy would bake in a fingerprint no clean
# checkout can reproduce — and the engine would then reject the very files we
# shipped, silently falling back to compiling from source on every client.
# Output goes to a directory of its own, never into the extracted tree's own
# third-party/compiled/: that copy comes from the index and still holds the
# PREVIOUS build, so writing over it in place would leave behind any bucket the
# current rules no longer produce (a filetype that lost its last rule, or one
# renamed by an engine fix) and ship it forever.
precompile:
	@tmp=$$(mktemp -d) && trap 'rm -rf "$$tmp"' EXIT && \
	  mkdir -p "$$tmp/src" && git checkout-index -a --prefix="$$tmp/src/" && \
	  CLEAVE_TRAITS_DIR="$$tmp/src" $(YARA_PRECOMPILE) "$$tmp/out" && \
	  rm -rf $(COMPILED_DIR) && mkdir -p $(COMPILED_DIR) && \
	  cp -R "$$tmp"/out/. $(COMPILED_DIR)/ && \
	  echo "Compiled YARA rules -> $(COMPILED_DIR)/ (from the staged tree)"

# Confirm the committed `.yrc` are exactly what this engine compiles from the
# committed rule sources — the same check pulsar runs before publishing, so a
# failure here is a bundle that would be refused at emit time. Byte-comparable
# because precompilation is deterministic. Slower and stricter than
# `check-precompile`: this one recompiles and catches corruption too.
verify-precompile:
	@tmp=$$(mktemp -d) && trap 'rm -rf "$$tmp"' EXIT && \
	  git archive --format=tar HEAD | tar -x -C "$$tmp" && \
	  CLEAVE_TRAITS_DIR="$$tmp" $(YARA_PRECOMPILE) "$$tmp/fresh" >/dev/null && \
	  diff -r "$$tmp/$(COMPILED_DIR)" "$$tmp/fresh" \
	    && echo "✓ committed YARA precompiles match the committed rule sources" \
	    || { echo "✗ committed YARA precompiles are stale — run 'make precompile'"; exit 1; }

# Fetch the latest third-party rule sources, then re-compile so the shipped
# `.yrc` always match the rules they were built from.
yara-update:
	cd third-party && "$(YARA_UPDATE)"
	$(MAKE) precompile

# Prior names, kept so existing scripts and muscle memory keep working.
yara-compile: precompile
yara-verify: verify-precompile

install-precommit:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	@echo "Pre-commit hook installed."
