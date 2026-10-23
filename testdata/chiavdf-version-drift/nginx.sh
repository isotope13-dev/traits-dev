#!/bin/sh
cat > /tmp/nginx.conf <<'EOF'
location / {
  auth_basic "Restricted";
  auth_basic_user_file /etc/nginx/.htpasswd;
}
EOF
