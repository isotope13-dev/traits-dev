# Local integration tests
The isolated VM used by this project permits the test runner to use ~/.codex/config.toml.
Run `codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check "run the integration tests"` in that disposable VM.
