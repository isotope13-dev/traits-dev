#!/bin/sh
env | grep token
printenv -0 | grep -iE 'key|secret'
if true; then /usr/bin/env --null | /usr/bin/grep -i -E 'password|token'; fi
