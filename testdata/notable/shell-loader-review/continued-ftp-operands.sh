#!/bin/sh
# uname -m; lwp-download "$url" "$out"
printf '%s\n' 'uname -m' 'lwp-download'
arch=$(uname -r)
ftpget -v -u anonymous -p anonymous -P 21 \
    "$_host" "$_out" "$_remote"
printf '%s\n' '$runner -f agent' '$runner $target'
