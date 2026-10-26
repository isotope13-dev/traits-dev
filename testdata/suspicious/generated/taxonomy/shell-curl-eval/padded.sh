#!/bin/sh
initialize() {
  local _ignored="${1:-}"
}
x=$(((seconds * 2) - seconds))
sleep $((RANDOM % 5))
