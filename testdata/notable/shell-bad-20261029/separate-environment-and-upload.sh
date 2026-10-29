#!/bin/sh
env | sort
printf '%s' healthy | curl --data-binary @- https://receiver.invalid/collect
