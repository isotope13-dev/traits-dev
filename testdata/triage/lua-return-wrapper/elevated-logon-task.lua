local command = "schtasks /create"
local trigger = "/sc onlogon"
local runlevel = "/rl highest"
return command .. " " .. trigger .. " " .. runlevel
