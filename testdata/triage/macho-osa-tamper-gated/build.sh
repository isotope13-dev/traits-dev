#!/bin/sh
# Compile static matcher fixtures. No generated code is executed.
set -eu
fixture_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
fixture_build=$(mktemp -d /tmp/macho-osa-controls.XXXXXX)
fixture_sdk=$(xcrun --sdk macosx --show-sdk-path)
for source_file in "$fixture_root"/controls/*.S; do
 fixture_name=$(basename "$source_file" .S)
 xcrun clang -target arm64-apple-macos13 -c "$source_file" -o "$fixture_build/$fixture_name.o"
 xcrun ld -arch arm64 -platform_version macos 13.0 26.0 -syslibroot "$fixture_sdk" -lSystem -e _main "$fixture_build/$fixture_name.o" -o "$fixture_root/controls/$fixture_name.macho"
done
