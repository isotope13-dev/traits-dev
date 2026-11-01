#!/bin/bash
# $'\x69\x64' -u
printf '%s\n' $'\x69\x64'
name=$'\x69\x64'
printf '%s\n' "$name"
printf '%s\n' "\$'\\x69\\x64' -u"
cat <<'DOC'
$'\x69\x64' -u
DOC
