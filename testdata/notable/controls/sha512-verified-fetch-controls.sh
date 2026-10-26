#!/usr/bin/env bash
# Verified multi-arch toolchain fetch (benign control): pins the SHA-512 of
# every artifact and checks it with sha512sum before use, then cleans up.
set -e
__ApkToolsVersion=2.12.11
__ApkToolsDir="$(mktemp -d)"
arch="$(uname -m)"
case "$arch" in
  x86_64) __ApkToolsSHA512SUM="53e57b49230da07ef44ee0765b9592580308c407a8d4da7125550957bb72cb59638e04f8892a18b584451c8d841d1c7cb0f0ab680cc323a3015776affaa3be33" ;;
  aarch64) __ApkToolsSHA512SUM="9e2b37ecb2b56c05dad23d379be84fd494c14bd730b620d0d576bda760588e1f2f59a7fcb2f2080577e0085f23a0ca8eadd993b4e61c2ab29549fdb71969afd0" ;;
esac
if command -v wget &> /dev/null; then
    wget -O- https://gitlab.alpinelinux.org/api/v4/projects/5/packages/generic/v$__ApkToolsVersion/$arch/apk.static > "$__ApkToolsDir/apk.static"
else
    curl -SLO --create-dirs --output-dir "$__ApkToolsDir" "https://gitlab.alpinelinux.org/api/v4/projects/5/packages/generic/v$__ApkToolsVersion/$arch/apk.static"
fi
echo "$__ApkToolsSHA512SUM $__ApkToolsDir/apk.static" | sha512sum -c
APK_BIN="$__ApkToolsDir/apk.static"
chmod +x "$APK_BIN"
"$APK_BIN" --initdb add
rm -rf "$__ApkToolsDir"
