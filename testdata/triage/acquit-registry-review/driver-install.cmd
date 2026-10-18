@echo off
sc create hardware type= kernel binPath= "C:\Drivers\hardware.sys"
sc start hardware
