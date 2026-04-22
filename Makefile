.PHONY: validate install-precommit

validate:
	cleave --traits-dir . validate

install-precommit:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	@echo "Pre-commit hook installed."
