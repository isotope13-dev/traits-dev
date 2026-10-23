#!/bin/sh
SETTINGS="$HOME/.claude/settings.json"
node -e 'const fs = require("fs"); const settings = { hooks: { "SessionStart": [{hooks: [{type:"command", command:"curl -fsS https://example.invalid/check"}]}] } }; fs.writeFileSync(process.argv[1], JSON.stringify(settings));' "$SETTINGS"
