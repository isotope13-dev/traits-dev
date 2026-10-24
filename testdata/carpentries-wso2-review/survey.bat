@echo off
systeminfo > system.txt
netstat -a -o > network.txt
tasklist /v > processes.txt
