.PHONY: validate install-precommit

validate:
	CLEAVE_TRAITS_PATH=. cleave validate

install-precommit:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	@echo "Pre-commit hook installed."
