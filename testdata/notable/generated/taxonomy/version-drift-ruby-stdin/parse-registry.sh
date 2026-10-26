#!/bin/sh
curl -fsSL https://registry.npmjs.org/dd-trace/latest |
  ruby -rjson -e 'puts JSON.parse(STDIN.read).fetch("version")'
