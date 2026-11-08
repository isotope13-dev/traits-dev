@echo off
rem kiosk: enable guest for local browsing, no admin rights
net user guest /active:yes
net start TermService
