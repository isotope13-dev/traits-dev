@echo off
bcdedit /set {current} recoveryenabled Yes
bcdedit /set {current} bootstatuspolicy DisplayAllFailures
wmic shadowcopy list brief
