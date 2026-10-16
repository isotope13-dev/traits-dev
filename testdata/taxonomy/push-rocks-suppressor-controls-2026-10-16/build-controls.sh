#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cc -o "$HERE/auth-failure-elf" "$HERE/auth-failure.c"
as -o "$HERE/null-run.o" "$HERE/null-run.s"
ld -o "$HERE/null-run-elf" "$HERE/null-run.o"
as -o "$HERE/code-cave.o" "$HERE/code-cave.s"
ld -N -e _entry -o "$HERE/code-cave-elf" "$HERE/code-cave.o"
strip -s "$HERE/code-cave-elf"
clang --target=aarch64-linux-gnu -c -o "$HERE/svc-aarch64.o" "$HERE/svc-aarch64.s"
mkdir -p "$HERE/auth" "$HERE/null" "$HERE/cave"
cp "$HERE/auth-failure-elf" "$HERE/auth/mailer-bin_linux_amd64"
cp "$HERE/null-run-elf" "$HERE/null/mailer-bin_linux_amd64"
cp "$HERE/code-cave-elf" "$HERE/cave/mailer-bin_linux_amd64"
cp "$HERE/svc-aarch64.o" "$HERE/svc/mailer-bin_linux_amd64"
cp "$HERE/svc-aarch64.o" "$HERE/network/rustnetwork_linux_amd64"
