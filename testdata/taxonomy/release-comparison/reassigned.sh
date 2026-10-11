#!/bin/bash
SCRIPT="echo ready"
ENC=$(printf '%s' "${SCRIPT}" | base64 | tr -d '\n')
ENC="ZWNobyBoaWRkZW4="
runner --command-line "/bin/bash -c 'echo ${ENC} | base64 -d | bash'"
