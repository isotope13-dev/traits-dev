@echo off
REM Positive control: actually disables the Windows firewall via netsh.
netsh advfirewall set allprofiles state off
netsh firewall set opmode disable
