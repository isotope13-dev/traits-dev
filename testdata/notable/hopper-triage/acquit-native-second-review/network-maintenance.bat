@echo off
netsh wlan delete profile name=*
netsh interface set interface "Lab wireless" disable
