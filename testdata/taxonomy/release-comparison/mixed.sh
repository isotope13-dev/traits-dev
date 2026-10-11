#!/bin/bash
SCRIPT="echo ready"
ENC=$(printf '%s' "${SCRIPT}" | base64 | tr -d '\n')
runner --command-line "/bin/bash -c 'echo ${ENC} | base64 -d | bash'"
echo ZWNobyBoaWRkZW4= | base64 -d | bash
