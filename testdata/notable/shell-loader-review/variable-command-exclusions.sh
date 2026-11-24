#!/bin/sh
# These are forwarding wrappers and documentation arguments, not assembled launches.
"$runner" "$@"
$runner '$*'
$runner "$1"
"${runner}" "$0"
$runner --help
$runner usage
printf '%s\n' '$runner arm64'
