local bridge = rawget(_G, "comm_center")
local function handler(request) return {status="ok"} end
if type(bridge) == "table" then bridge["reg_service"]("health", handler) end
return bridge
