@echo off
jmap -dump:format=b,file=%TEMP%\heap.bin %PID%
jstack %PID% > threads.txt
