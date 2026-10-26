#!/bin/sh
B="/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Cache"
if [ ! -d "$B" ]; then mkdir -p "$B"; fi
if [ -f "$W/index" ]; then cp "$W/index" "$B/index"; fi
