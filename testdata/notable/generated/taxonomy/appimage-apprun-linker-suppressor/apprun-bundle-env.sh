#!/usr/bin/env bash
# Benign control: AppImage AppRun-style launcher. Resolving the bundle root
# from its own path and pointing the loader at bundled libraries plus the
# union-preload shim is the documented AppImage runtime mechanism.
HERE="$(dirname "$(readlink -f "${0}")")"

export PATH="${HERE}"/usr/bin/:"${PATH}"
export LD_LIBRARY_PATH="${HERE}"/usr/lib/:"${HERE}"/lib/:"${LD_LIBRARY_PATH}"
export LD_PRELOAD="${HERE}/libunionpreload.so"

chmod a+x AppRun
ls -lh ../out/*.AppImage
