#!/bin/sh
curl -fsS http://1.1.1.1/cdn-cgi/trace
nohup /usr/bin/sleep 60 >job.log 2>&1 &
