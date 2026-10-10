local command = "schtasks /create /sc daily /st 12:00 /f"
local action = '/tn maintenance /tr "maintenance.exe"'
return command .. " " .. action
