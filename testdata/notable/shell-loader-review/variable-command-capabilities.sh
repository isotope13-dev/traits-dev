#!/bin/sh
arch=$(uname -m 2>/dev/null | tr A-Z a-z)
lwp-download "$url" "$out"
"$runner" "$target"
${runner} ${target}
$runner -f agent
