#!/bin/sh
cat > /usr/bin/netstat <<'NETSTAT'
#!/bin/sh
busybox netstat "$@" | grep -v '^Proto'
NETSTAT
chmod +x /usr/bin/netstat
