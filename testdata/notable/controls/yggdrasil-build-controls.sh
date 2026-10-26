#!/bin/bash
# BinaryBuilder-style macOS SDK sysroot refresh (cf. Yggdrasil
# build_tarballs.jl): replace the STAGED sysroot's System subtree with a
# fresh SDK extract. The deleted System lives under the staging prefix, it
# is not the running macOS /System directory.
SYSROOT="/opt/${target}/${target}/sys-root"
rm -rf "${SYSROOT}/System" "${SYSROOT}/usr/include/libxml2"
tar --extract --file="${WORKSPACE}/srcdir/MacOSX13.3.tar.xz" --directory="${SYSROOT}/." --strip-components=1 MacOSX13.3.sdk/System MacOSX13.3.sdk/usr

# Self-named wrapper dispatch (cf. Yggdrasil G/Git/build_tarballs.jl): the
# `git` driver re-execs its renamed sibling while keeping its OWN argv[0],
# preserving identity rather than masquerading as another process.
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
exec -a "${BASH_SOURCE[0]}" "${SCRIPT_DIR}/_git" "$@"

