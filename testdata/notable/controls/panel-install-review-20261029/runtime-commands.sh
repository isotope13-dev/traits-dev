#!/bin/sh
ruby -e 'puts "probe"'
printf 'puts "probe"' | ruby -e 'eval(STDIN.read)'
node -r ./loader.js ./tool.jsc
printf data | curl --data-binary @- https://example.org/import
url="https://example.org/fetch?url=https://example.net/image.png"
port=443
printf '\033[32mready\033[0m\n'
source "$runtime_path"
