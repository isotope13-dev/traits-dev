#!/bin/sh
LABEL=$(echo 'hello' | tr 'a-z' 'A-Z')
COMMAND='printf "%s\n" "$LABEL"'
eval "$COMMAND"
exec sh -c 'printf OK'
