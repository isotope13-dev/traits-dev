CLEAVE ?= $(if $(wildcard ../cleave/target/release/cleave),../cleave/target/release/cleave,cleave)
YARA_PRECOMPILE ?= $(if $(wildcard ../cleave/target/release/yara-precompile),../cleave/target/release/yara-precompile,yara-precompile)
YARA_UPDATE ?= $(abspath $(if $(wildcard ../cleave/tools/yara-update/yara-update),../cleave/tools/yara-update/yara-update,yara-update))

.PHONY: validate install-precommit yara-update yara-compile

validate:
	$(CLEAVE) --traits-dir . validate

# Compile the third-party + built-in YARA rules into portable per-filetype
# `.yrc` files (plus a manifest) under third-party/compiled/. These ship inside
# the trait package; cleave loads them at runtime with no in-process
# compilation. The `.yrc` hold WASM bytecode, so one build is loadable on every
# client architecture and OS.
yara-compile:
	CLEAVE_TRAITS_DIR=$(CURDIR) $(YARA_PRECOMPILE) third-party/compiled
	@echo "Compiled YARA rules -> third-party/compiled/"

# Fetch the latest third-party rule sources, then re-compile so the shipped
# `.yrc` always match the rules they were built from.
yara-update:
	cd third-party && "$(YARA_UPDATE)"
	$(MAKE) yara-compile

install-precommit:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	@echo "Pre-commit hook installed."
