#!/bin/sh
# don't want to modprobe $MODNAME automatically, so give user a hint
CONFIG=/proc/config.gz
if [ -r "$CONFIG" ]; then
    zcat "$CONFIG" | grep -q '^CONFIG_NAMESPACES=y'
else
    echo "Try modprobe $MODNAME module, or check /boot/config-$(uname -r)" >&2
fi
