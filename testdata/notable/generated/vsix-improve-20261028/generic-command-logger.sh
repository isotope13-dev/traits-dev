#!/bin/sh
command_text="$1"
sensitive_path="/tmp/activity.log"
printf '%s\n' "$command_text" >> "$sensitive_path"
