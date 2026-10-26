#!/bin/sh
# Dev-environment exporter: materialize the Nix developer environment into
# $GITHUB_ENV for later CI steps. Runner controls and transient shell state
# are never exported.
dev_env="$RUNNER_TEMP/dune-dev-env.json"
nix print-dev-env path:. --json > "$dev_env"
python3 - "$dev_env" "$GITHUB_ENV" <<'PY'
import json
import secrets
import sys

with open(sys.argv[1]) as source:
    variables = json.load(source)["variables"]

# print-dev-env contains derivation variables, not the ambient runner
# environment. Preserve runner controls and transient shell state.
excluded = {
    "BASH_ENV",
    "CI",
    "HOME",
    "TMPDIR",
}

with open(sys.argv[2], "a") as output:
    for name, variable in variables.items():
        if variable["type"] != "exported" or name in excluded:
            continue
        if name.startswith(("ACTIONS_", "GITHUB_", "RUNNER_")):
            continue
        value = variable["value"]
        delimiter = f"__NIX_ENV_{secrets.token_hex(16)}__"
        output.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")
PY
