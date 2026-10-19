local daily = "schtasks /create /sc daily /st 12:00 /f"
local action = ' /tn Maintenance /tr "C:/Tools/maintenance.exe"'
return daily .. action
