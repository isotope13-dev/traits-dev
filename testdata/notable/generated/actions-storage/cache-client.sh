#!/bin/bash
TW="${ACTIONS_RESULTS_URL%/}/twirp/github.actions.results.api.v1.CacheService"
curl -sS -X POST "$TW/CreateCacheEntry" -d '{"key":"build-cache","version":"1"}'
curl -sS -X PUT "$signed_url" --data-binary @build.tgz
curl -sS -X POST "$TW/FinalizeCacheEntryUpload" -d '{"key":"build-cache","size_bytes":"1024","version":"1"}'
