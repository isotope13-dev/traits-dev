@echo off
vssadmin list shadows
wbadmin get versions
bcdedit /enum
