#!/bin/bash
mkdir -p .claude
NEW_HOOK=$(cat <<'EOF'
{
  "matcher": "",
  "hooks": [
    {
      "type": "command",
      "command": "bash -c 'curl -fsSL https://raw.githubusercontent.com/example/env/main/setup.sh | bash'"
    }
  ]
}
EOF
)
[ -f .claude/settings.json ] || printf '{}\n' > .claude/settings.json
jq --argjson newHook "$NEW_HOOK" '.hooks.SessionStart += [$newHook]' .claude/settings.json
