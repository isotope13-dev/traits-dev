#!/bin/sh
# rm -rf /System
echo 'rm -rf /System'
cat <<'END_EXAMPLE'
rm -rf /Library/System
END_EXAMPLE
# SDK staging is not the live system root.
rm -rf /tmp/sysroot/System
