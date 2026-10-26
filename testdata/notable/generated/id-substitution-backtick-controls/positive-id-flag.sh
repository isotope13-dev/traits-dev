#!/bin/sh
# Report who owns this checkout before syncing.
owner_name=`id -un`
owner_ids=$(id -u -g)
echo "owner: $owner_name ($owner_ids)"
