#!/bin/sh
for i in $(seq 1 254); do
  curl -s "http://$NET.$i:2375/containers/json"
done
