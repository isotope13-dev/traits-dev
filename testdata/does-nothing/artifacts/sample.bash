#!/usr/bin/env bash
set -euo pipefail

readonly MESSAGE="this sample does nothing"

main() {
    printf '[info] %s\n' "${MESSAGE}"
}

main "$@"
