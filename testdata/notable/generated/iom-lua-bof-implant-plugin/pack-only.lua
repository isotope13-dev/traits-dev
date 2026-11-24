-- Packs arguments and rates a command, but never dispatches a BOF to a session
local function pack_only(args, cmd)
    local packed_args = bof_pack("z", "check")
    return packed_args
end

opsec("check_only", 1.0)
