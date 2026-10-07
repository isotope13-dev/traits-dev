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

.PHONY: validate taxonomy-check precompile yara-compile yara-update install-precommit

# Rule validation.
#
# Nothing here gates on third-party/compiled/. Those artifacts are built into a
# published bundle, not committed, and a stale or absent `.yrc` set is inert at
# runtime anyway -- the engine ignores it and compiles from source, so the
# failure mode is a slower client, not a wrong verdict.
# Validate each fixture independently, including byte-identical files whose
# names select different traits (for example, build.rs versus lib.rs).
validate:
	$(CLEAVE) --traits-dir . validate

# Taxonomy-migration checks (NEW_TAXONOMY_PLAN.md). Python-based and depends on
# untracked scripts/, so it is kept out of `validate`.
taxonomy-check:
	uv run --with pyyaml python scripts/test-taxonomy-move.py
	python3 scripts/test-taxonomy-corpus-comparison.py
	python3 scripts/taxonomy_sources.py
	python3 scripts/check-taxonomy-memory-map.py --cleave "$(CLEAVE)"
	python3 taxonomy-migration/batches/120-ruby-module-load/run-focused-cases.py --cleave "$(CLEAVE)"
	python3 taxonomy-migration/batches/121-credential-schema/run-focused-cases.py --cleave "$(CLEAVE)"
	python3 taxonomy-migration/batches/122-credential-source-symbols/run-focused-cases.py --cleave "$(CLEAVE)"
	python3 taxonomy-migration/batches/123-ruby-reflection/run-focused-cases.py --cleave "$(CLEAVE)"
	python3 taxonomy-migration/batches/124-go-reflection/run-focused-cases.py --cleave "$(CLEAVE)"
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/125-ruby-variation-key-components/cases.json --compare taxonomy-migration/batches/125-ruby-variation-key-components/evidence-before.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/memory-operations/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/memory-lifecycle/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/memory-catalog/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/windows-heap/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/decompression/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/compression-boundaries/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/compression-mode/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/web-codec-streams/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/033-github-recursive-tree-option/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/compression-family/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/python-zlib-import-metadata/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/zlib-software-name-metadata/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/zstd-software-name-metadata/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/lzma-import-metadata/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/codec-directions/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/codec-neutral/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/codec-zlib/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/codec-zstd/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/bzip2-boundaries/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/powershell-gzip-staging/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/034-powershell-encoded-command-precision/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/container-privilege/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/036-input-capture-mbc-correction/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/040-shell-input-attack-mapping/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/038-homebrew-transfer-claims/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/039-pastebin-dispatch-claim/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/041-npm-hook-b0024/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/042-email-spam-mapping/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/043-paste-eval-precision/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/044-driver-mapping-corrections/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/045-registry-config-mappings/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/046-conditional-execution-mappings/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/047-network-port-home/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/048-domain-home/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/049-limit-home/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/050-selector-precision/port-consumers/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/050-selector-precision/empire-http-consumers/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/052-per-page-option-disposition/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/053-channel-domain-identifier/cases-after.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/054-architecture-strings/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/055-accounting-vocabulary/cases-after.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/credential-text/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/057-charset-home/cases-encoding-after.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/058-cicd-vocabulary/cases-after.json
	python3 taxonomy-migration/batches/059-identity-strings/check-phishing-selector-cases.py --cleave "$(CLEAVE)" --traits-dir . --phase after
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/061-process-name-strings/061c-telnet-basename/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/061-process-name-strings/061b-target-name-audit/cases.json
	python3 taxonomy-migration/batches/063-file-strings/check-path-context-cases.py --cleave "$(CLEAVE)" --traits-dir . --phase after
	python3 taxonomy-migration/research/b101-suite-workspace/check-b064-current.py --cleave "$(CLEAVE)" --traits-dir .
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/064-security-strings/follow-up-scanning/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/066-account-strings/cases-after.json
	python3 taxonomy-migration/batches/067-container-strings/check-candidate-cases.py --cleave "$(CLEAVE)" --traits-dir . --phase after
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/069-artifact-strings/cases-after.json
	python3 taxonomy-migration/batches/072-collection-strings/retirement/check-after.py .
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/073-form-validation-strings/cases-after.json
	python3 taxonomy-migration/batches/074-corpus-strings/js-fetch-candidate/check-focused-after.py --cleave "$(CLEAVE)" --traits-dir .
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/076-command-strings/binding-retirement/cases-after.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/078-charset-strings/cases-after.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/079-credential-strings/uppercase-candidate/cases-after.json
	python3 taxonomy-migration/batches/079-tool-auth-suppressor/check-cases.py --cleave "$(CLEAVE)"
	python3 taxonomy-migration/batches/080-vscode-encodedcommand-selector/check-cases.py --cleave "$(CLEAVE)"
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/062-identity-suppressor-precision/follow-up-empty-join/cases-after.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/062-identity-suppressor-precision/follow-up-batch-metric/cases-after.json
	python3 taxonomy-migration/batches/074-corpus-strings/route-post-followup/check-focused-after.py --traits-dir . --cleave "$(CLEAVE)"
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/cipher-directions-current/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/091-qos-objective-retirement/cases-after.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/089-wfp-source-call-precision/cases-after.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases testdata/taxonomy/command-task-field/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/098-reviewed-paths-with-image/image-cases-after.json
	python3 taxonomy-migration/research/b098-frozen-suite-workspace/check-time-after.py --cleave "$(CLEAVE)"
	python3 taxonomy-migration/research/b101-suite-workspace/run-after-controls.py --cleave "$(CLEAVE)" --traits-dir .
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/102-current-file-populations/focused-cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/130-java-accessibility/cases.json
	python3 scripts/check-taxonomy-cases.py --cleave "$(CLEAVE)" --cases taxonomy-migration/batches/131-powershell-decryptor-home/cases.json

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
