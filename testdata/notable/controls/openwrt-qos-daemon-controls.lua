-- OpenWrt firmware-tree Lua daemon control: nixio/luci bindings, helper
-- subprocess reads, kernel device-node writes, dofile library loading.
-- None of that is file infection.
local uci = require "luci.model.uci"
local nfs = require "nixio.fs"

local DEV_CTL = "/dev/qos_ctl"

local function read_helper(command)
	local fp = io.popen(command .. " 2>/dev/null")
	local out = fp:read("*a")
	fp:close()
	return out
end

local function push_policy(blob)
	local fp = io.open(DEV_CTL, "w")
	fp:write(blob)
	fp:close()
end

-- classifier helpers ship as Lua on some targets, require-able on others
local ok, mod = pcall(require, "qosrules")
if not ok then
	local path
	for _, dir in ipairs({ "/usr/share/qos/", "/etc/qos/" }) do
		path = dir .. "qosrules.lua"
		local probe = io.open(path, "r")
		if probe then
			probe:close()
			ok, mod = pcall(dofile, path)
			if ok then
				break
			end
		end
	end
end

push_policy(read_helper("qos-dump"))
