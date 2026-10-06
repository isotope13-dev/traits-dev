-- Positive control: subprocess plus write-mode open plus naming Lua
-- targets with no platform context must still trip the infector rule.
local function spread(target)
	local fp = io.popen("ls /tmp/*.lua")
	for name in fp:lines() do
		local out = io.open(name, "w")
		out:write("-- patched by spreader\n")
		out:close()
	end
	fp:close()
	local lib = io.open(target, "r")
	if lib then
		lib:close()
	end
end

spread("/tmp/victim.lua")
