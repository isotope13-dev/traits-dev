#!/bin/sh
# locate the original script; do not delete the source map.
sed -i 's/^[[:space:]]*rm.*PACKAGER_SOURCEMAP_FILE/#&/' "$REACT_NATIVE_XCODE"
