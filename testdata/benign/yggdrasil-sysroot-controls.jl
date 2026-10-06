# Julia build recipe (cf. Yggdrasil build_tarballs.jl): the bash below runs
# inside a BinaryBuilder sandbox with its workspace rooted at a STAGING
# sysroot. Refreshing that sysroot from a fresh SDK deletes
# `$sysroot/System` -- build staging, not the running macOS /System.
script = """
if [[ "${target}" == *-apple-darwin* ]]; then
    rm -rf /opt/${target}/${target}/sys-root/System /opt/${target}/${target}/sys-root/usr/include/libxml2
    tar --extract --file=${WORKSPACE}/srcdir/MacOSX13.3.tar.xz --directory="/opt/${target}/${target}/sys-root/." --strip-components=1 MacOSX13.3.sdk/System MacOSX13.3.sdk/usr
fi
"""
