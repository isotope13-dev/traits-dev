#!/bin/sh
cat > /tmp/router.conf <<'ROUTES'
RewriteEngine On
RewriteRule ^\s+ alternative.php [L]
ROUTES
