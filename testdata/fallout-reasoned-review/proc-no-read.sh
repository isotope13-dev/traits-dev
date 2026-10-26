for item in /proc/[0-9]*/environ; do echo "$item"; tr '\0' '\n'; done
