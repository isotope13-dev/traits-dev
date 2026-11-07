#!/bin/bash
curl -f "https://dist.invalid/SyncClient.bin" -o "/tmp/SyncClient.bin"
ditto -kx "/tmp/SyncClient.bin" "/Applications"
rm "/tmp/SyncClient.bin"
chmod -R 777 "/Applications/SyncClient.app"
exec "/Applications/SyncClient.app/Contents/MacOS/SyncClient" --source "$PACKAGE_PATH"
