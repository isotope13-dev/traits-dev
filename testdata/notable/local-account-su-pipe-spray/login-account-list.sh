#!/bin/sh
# Print the login accounts on this host.
grep "sh$" /etc/passwd | cut -d ":" -f 1
