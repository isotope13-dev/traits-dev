#!/bin/sh
cat > /tmp/upgrade-helper.sh <<EOF
echo ready
EOF
crictl pods
