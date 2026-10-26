printf '%s\n' /proc/[0-9]*/environ
tr '\0' '\n' < "$other"
