#!/bin/sh
cat <<'COMMANDS'
ruby -e 'system("ruby", "validate.rb")'
COMMANDS
echo 'ruby -e exec("echo example")'
