local daily = "schtasks /create /sc daily /st 12:00 /f"
local name = "/tn Maintenance"
local unrelated = "rundll32 shell32.dll,Control_RunDLL"
return daily, name, unrelated
