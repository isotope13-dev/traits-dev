for item in /proc/[0-9]*/environ; do tr '\0' '\n' < "$other"; done
