#!/bin/sh
value=$(printf abcXdef | tr -d X)
printf '%s\n' "$value"
