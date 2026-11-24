#!/bin/sh
# Benign context in another command must not hide a variable launch.
"$wrapper" "$@"
$wrapper --help
$stage arm64
"${stage}" "$tag"
