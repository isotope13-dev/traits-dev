CLEAVE ?= $(if $(wildcard ../cleave/target/release/cleave),../cleave/target/release/cleave,cleave)
# Honor the selected engine in helpers that consume CLEAVE from the environment.
export CLEAVE
YARA_PRECOMPILE ?= $(or $(wildcard ../cleave/target/release/yara-precompile),$(wildcard $(dir $(CLEAVE))../cleave/target/release/yara-precompile),$(wildcard /var/lib/cyclotron/cleave/target/release/yara-precompile),$(shell command -v yara-precompile 2>/dev/null),yara-precompile)
# Prefer the installed CLI; fall back to a sibling cleave checkout's build.
# `go run github.com/atomdrift-project/cleave/tools/yara-update@latest` does not
# work today: that directory declares `module yara-update`, so the import path
# the repo layout implies isn't the module's own path.
YARA_UPDATE ?= $(if $(shell command -v yara-update 2>/dev/null),yara-update,$(abspath ../cleave/tools/yara-update/yara-update))

COMPILED_DIR := third-party/compiled

.PHONY: validate validate-uncached validate-profile precompile yara-compile yara-update install-precommit test-vsix-withdrawal test-bound-opener test-python-openers test-xpi-triage-good test-swift-triage-good

# Offline dependency/registry regressions, including a consuming VSIX. Uses
# synthetic provider responses in its own cache; never runs package code.
ATOMSCAN ?= ../scan/target/release/atomscan
WITHDRAWAL_TEST_WORK ?= $(CURDIR)/.triage-work/vsix-withdrawal-regression
test-vsix-withdrawal:
	python3 scripts/review/test-vsix-withdrawal.py --atomscan "$(ATOMSCAN)" --work-dir "$(WITHDRAWAL_TEST_WORK)"

test-bound-opener:
	python3 scripts/review/test-bound-opener.py

test-python-openers:
	python3 scripts/review/test-python-openers.py

.PHONY: test-go-handler-command-context
test-go-handler-command-context:
	python3 scripts/review/test-go-handler-command-context.py

.PHONY: test-openssl-aes-direction
test-openssl-aes-direction:
	python3 scripts/review/test-openssl-aes-direction.py

test-xpi-triage-good:
	python3 scripts/review/test-xpi-triage-good.py --cleave "$(CLEAVE)"

test-swift-triage-good:
	python3 scripts/review/test-swift-triage-good.py --cleave "$(CLEAVE)"

.PHONY: test-npm-triage-good
test-npm-triage-good:
	python3 scripts/review/test-npm-triage-good.py --cleave "$(CLEAVE)"

.PHONY: test-npm-improve
test-npm-improve:
	python3 scripts/review/test-npm-improve.py --cleave "$(CLEAVE)"

.PHONY: test-npm-triage-bad
test-npm-triage-bad:
	python3 scripts/review/test-npm-triage-bad.py --cleave "$(CLEAVE)"

.PHONY: test-npm-bad-improve
test-npm-bad-improve:
	python3 scripts/review/test-npm-bad-improve.py --cleave "$(CLEAVE)"

.PHONY: test-nupkg-triage-good
test-nupkg-triage-good:
	python3 scripts/review/test-nupkg-good-triage.py --cleave "$(CLEAVE)"

.PHONY: test-nupkg-improve
test-nupkg-improve:
	python3 scripts/review/test-nupkg-improve.py --cleave "$(CLEAVE)"

.PHONY: test-nupkg-triage-bad test-nupkg-host-query
test-nupkg-triage-bad:
	python3 scripts/review/test-nupkg-bad-triage.py --cleave "$(CLEAVE)"

test-nupkg-host-query:
	python3 scripts/review/test-nupkg-host-query.py --cleave "$(CLEAVE)"

.PHONY: test-swift-archive-improve
test-swift-archive-improve:
	python3 scripts/review/test-swift-archive-improve.py --cleave "$(CLEAVE)"

# Rule validation.
#
# Nothing here gates on third-party/compiled/. Those artifacts are built into a
# published bundle, not committed, and a stale or absent `.yrc` set is inert at
# runtime anyway -- the engine ignores it and compiles from source, so the
# failure mode is a slower client, not a wrong verdict.
# Validate each fixture independently, including byte-identical files whose
# names select different traits (for example, build.rs versus lib.rs).
# Reports are keyed on content, filename/type, analysis options, engine build,
# and trait content, with path-equivalence checks before reuse. Reuse unchanged
# successful full-validation results for iteration. A fresh run measures rule
# costs without analysis-report reuse; --soft reports performance issues without
# failing. Every classified fixture also supplies a measured cost probe.
# validate-uncached forces a fresh measured pass.
validate:
	$(CLEAVE) --traits-dir . validate

validate-uncached:
	CLEAVE_SKIP_CACHE=1 $(CLEAVE) --traits-dir . validate

# Aggregate regex/Tree-sitter trait costs and slow fixtures. Avoid --verbose:
# it also computes the expensive, unrelated fixture-overlap diagnostic.
# Requires cleave's validate scan-stat reporting; output goes to stderr.
SLOW_RULE_MS ?= 500
validate-profile:
	CLEAVE_SKIP_CACHE=1 CLEAVE_TRAIT_TIMING=1 CLEAVE_PHASE_STATS=1 RUST_LOG=cleave=info $(CLEAVE) --slow-rule-ms $(SLOW_RULE_MS) --traits-dir . validate

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
# MIME filetype buckets such as application/x-zsh need their output parent.
precompile:
	@tmp=$$(mktemp -d) && trap 'rm -rf "$$tmp"' EXIT && \
	  mkdir -p "$$tmp/src" "$$tmp/out/application" && git checkout-index -a --prefix="$$tmp/src/" && \
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

.PHONY: test-lua-triage-good
test-lua-triage-good:
	python3 scripts/review/test-lua-triage-good.py --cleave "$(CLEAVE)"

.PHONY: test-lua-triage-bad
test-lua-triage-bad:
	python3 scripts/review/test-lua-triage-bad.py --cleave "$(CLEAVE)"

.PHONY: test-lua-bad-improve
test-lua-bad-improve:
	python3 scripts/review/test-lua-bad-improve.py --cleave "$(CLEAVE)"

.PHONY: test-lua-generated-source
test-lua-generated-source:
	python3 scripts/review/test-lua-generated-source.py --cleave "$(CLEAVE)"

.PHONY: test-lua-process-configuration
test-lua-process-configuration:
	python3 scripts/review/test-lua-process-configuration.py --cleave "$(CLEAVE)"

.PHONY: test-local-command-taxonomy
test-local-command-taxonomy:
	python3 scripts/review/test-local-command-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-remote-admin-taxonomy
test-remote-admin-taxonomy:
	python3 scripts/review/test-remote-admin-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-shortcut-target-taxonomy
test-shortcut-target-taxonomy:
	python3 scripts/review/test-shortcut-target-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-process-start-taxonomy
test-process-start-taxonomy:
	python3 scripts/review/test-process-start-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-hidden-window-taxonomy
test-hidden-window-taxonomy:
	python3 scripts/review/test-hidden-window-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-shell-handler-taxonomy
test-shell-handler-taxonomy:
	python3 scripts/review/test-shell-handler-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-scanner-taxonomy-suppression
test-scanner-taxonomy-suppression:
	python3 scripts/review/test-scanner-taxonomy-suppression.py --cleave "$(CLEAVE)"

.PHONY: test-go-command-start
test-go-command-start:
	python3 scripts/review/test-go-command-start.py --cleave "$(CLEAVE)"

.PHONY: test-response-model-context
test-response-model-context:
	python3 scripts/review/test-response-model-context.py --cleave "$(CLEAVE)"

.PHONY: test-stream-cipher-taxonomy
test-stream-cipher-taxonomy:
	python3 scripts/review/test-stream-cipher-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-url-path-taxonomy
test-url-path-taxonomy:
	python3 scripts/review/test-url-path-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-memory-allocation-taxonomy
test-memory-allocation-taxonomy:
	python3 scripts/review/test-memory-allocation-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-child-process-taxonomy
test-child-process-taxonomy:
	python3 scripts/review/test-child-process-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-python-os-alias-taxonomy
test-python-os-alias-taxonomy:
	python3 scripts/review/test-python-os-alias-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-java-collection-exfiltration
test-java-collection-exfiltration:
	python3 scripts/review/test-java-collection-exfiltration.py --cleave "$(CLEAVE)"

.PHONY: test-process-config-taxonomy
test-process-config-taxonomy:
	python3 scripts/review/test-process-config-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-interpreter-input-taxonomy
test-interpreter-input-taxonomy:
	python3 scripts/review/test-interpreter-input-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-node-inline-taxonomy
test-node-inline-taxonomy:
	python3 scripts/review/test-node-inline-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-interpreter-config-taxonomy
test-interpreter-config-taxonomy:
	python3 scripts/review/test-interpreter-config-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-background-job-taxonomy
test-background-job-taxonomy:
	python3 scripts/review/test-background-job-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-python-inline-position
test-python-inline-position:
	python3 scripts/review/test-python-inline-position.py --cleave "$(CLEAVE)"

.PHONY: test-allocation-api-consumers
test-allocation-api-consumers:
	python3 scripts/review/test-allocation-api-consumers.py --cleave "$(CLEAVE)"

.PHONY: test-applescript-subject-taxonomy
test-applescript-subject-taxonomy:
	python3 scripts/review/test-applescript-subject-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-wsh-evidence-taxonomy
test-wsh-evidence-taxonomy:
	python3 scripts/review/test-wsh-evidence-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-gradle-command-taxonomy
test-gradle-command-taxonomy:
	python3 scripts/review/test-gradle-command-taxonomy.py --cleave "$(CLEAVE)"

.PHONY: test-script-automation-taxonomy
test-script-automation-taxonomy:
	python3 scripts/review/test-script-automation-taxonomy.py --cleave "$(CLEAVE)"
