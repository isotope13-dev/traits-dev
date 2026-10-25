@echo off
takeown /f C:\Windows\System32\drivers\etc\hosts
icacls C:\Windows\System32\drivers\etc\hosts /inheritance:r /grant:r Everyone:F
attrib +R C:\Windows\System32\drivers\etc\hosts
