#!/bin/sh
# Print a template for operators; no access-control file is written.
cat <<'HELP'
Place administrator-approved public keys in authorized_keys.
Example (truncated): ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI35bbad comment
HELP
