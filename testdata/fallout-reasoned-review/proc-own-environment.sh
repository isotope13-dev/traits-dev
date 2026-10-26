for item in /proc/self/environ; do tr '\0' '\n' < "$item"; done
