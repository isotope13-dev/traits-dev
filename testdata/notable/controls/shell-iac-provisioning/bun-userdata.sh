#!/bin/bash
# EC2 user-data fragment: install Bun and persist its PATH for login shells.
# The official Bun installer shape (curl-piped setup writing BUN_INSTALL to
# the shell rc) is provisioning, not rc persistence by malware.
curl -fsSL https://bun.sh/install | bash
echo 'export BUN_INSTALL="/root/.bun"' >> /root/.bashrc
echo 'export PATH="$BUN_INSTALL/bin:$PATH"' >> /root/.bashrc
source /root/.bashrc
