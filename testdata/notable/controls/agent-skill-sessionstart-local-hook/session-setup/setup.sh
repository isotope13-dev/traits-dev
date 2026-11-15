#!/bin/bash
mkdir -p .claude
cat > .claude/settings.json <<'EOF'
{"hooks":{"SessionStart":[{"hooks":[{"type":"command","command":"bash ~/.claude/hooks/session-start.sh"}]}]}}
EOF
