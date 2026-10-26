#!/bin/bash
SCRIPT="echo ready"
ENC=$(printf '%s' "${SCRIPT}" | base64 | tr -d '\n')
runner --command-line "/bin/bash -c 'echo ${PAYLOAD} | base64 -d | bash'"
