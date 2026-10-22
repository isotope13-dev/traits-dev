#!/bin/sh
curl -fsSL https://updates.invalid/metadata.json > versions.json
ruby -rjson -e 'puts JSON.parse(File.read("versions.json"))'
