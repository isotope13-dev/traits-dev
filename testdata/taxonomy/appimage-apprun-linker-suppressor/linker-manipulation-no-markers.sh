#!/usr/bin/env bash
# Malicious control: linker manipulation with no AppImage markers. Setting
# both the library search path and a preloaded object from a world-writable
# staging directory must still convict.
export LD_LIBRARY_PATH="/tmp/.staging/lib:${LD_LIBRARY_PATH}"
export LD_PRELOAD="/tmp/.staging/libevil.so"
exec "$@"
