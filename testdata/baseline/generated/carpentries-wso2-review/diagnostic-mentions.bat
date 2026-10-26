@echo off
REM jmap -dump:format=b,file=x.bin %PID%
echo jstack %PID%
jstack --help
jmap -histo %PID%
