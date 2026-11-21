#!/bin/bash
CACHEAPIS="${ACTIONS_CACHE_URL}_apis/artifactcache"
curl -sS -X PATCH "$CACHEAPIS/caches/$CID" --data-binary @build.tgz
