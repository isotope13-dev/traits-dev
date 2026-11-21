#!/bin/sh
# A local hook configuration and a separate one-time installer.
printf '%s\n' '{"hooks":{"SessionStart":[{"hooks":[{"type":"command","command":"./local-hook.sh"}]}]}}'
printf '%s\n' 'Installing an unrelated tool'
printf '%s\n' 'This download is outside the hook command'
curl -fsSL https://example.org/install.sh | sh
