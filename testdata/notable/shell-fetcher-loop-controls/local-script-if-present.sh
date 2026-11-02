#!/bin/sh
# Control: runs a locally installed helper when present. The conditional
# execution shape matches the dropper's final step, but nothing is
# downloaded and no fetcher list is involved.
HELPER="$HOME/.local/bin/helper"
if [ -f $HELPER ]; then sh $HELPER --init; fi
