#!/bin/sh
cat > /usr/bin/netstat <<'NETSTAT'
#!/bin/sh
busybox netstat "$@"
NETSTAT
chmod +x /usr/bin/netstat
