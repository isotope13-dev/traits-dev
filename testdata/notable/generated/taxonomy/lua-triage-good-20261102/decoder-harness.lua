-- deob.lua — poisoned-environment instrumented loader for uix.txt
-- The pure-Lua decoder (string/table/math) runs for real; every outward effect
-- (os/io/require/ffi/loadstring) is intercepted at the env boundary, its arguments
-- logged, and replaced with an inert stub. Nothing the payload "does" actually happens.
--
-- Usage (inside a disposable, network-less VM):  luajit deob.lua uix.txt
-- Outputs:  deob.log  (every API the payload resolved + its arguments)
--           stage2.NN.lua  (any decoded child chunk captured as plaintext)

local SRC_PATH = arg[1] or "uix.txt"

local f = assert(io.open(SRC_PATH, "rb"))
local src = f:read("*a"); f:close()

local function ser(v, depth)
  depth = depth or 0
  local t = type(v)
  if t == "string" then
    if #v > 400 then return string.format("<str %dB %q...>", #v, v:sub(1, 400)) end
    return string.format("%q", v)
  elseif t == "table" and depth < 1 then
    local parts = {}
    for k, val in pairs(v) do parts[#parts + 1] = tostring(k) .. "=" .. ser(val, depth + 1) end
    return "{" .. table.concat(parts, ", ") .. "}"
  else
    return tostring(v)
  end
end

local logf = assert(io.open("deob.log", "w"))
-- Op budget: the permissive proxy lets pointer/handle chains flow forever, so a
-- loop over fake handles never terminates. Cap total records and unwind via error
-- once the behavioral surface is captured — pcall catches it, all dumps survive.
local BUDGET, ops = 40000, 0
local function rec(kind, ...)
  ops = ops + 1
  if ops > BUDGET then error("op-budget reached (" .. BUDGET .. ")", 0) end
  local n, parts = select("#", ...), {}
  for i = 1, n do parts[i] = ser((select(i, ...))) end
  logf:write(kind .. "\t" .. table.concat(parts, "\t") .. "\n")
end

local chunk_n = 0
local function capture_chunk(s)
  chunk_n = chunk_n + 1
  local p = string.format("stage2.%02d.lua", chunk_n)
  if type(s) == "string" then
    local cf = io.open(p, "w"); cf:write(s); cf:close()
    rec("LOADSTRING_CAPTURED", "->" .. p, #s .. "B")
  else
    rec("LOAD_READER_FN", p)  -- load() given a function reader; cannot dump statically
  end
  return function() rec("CHILD_CHUNK_INVOKED", p); return nil end
end

local function stub(name)
  return function(...) rec("CALL", name, ...); return nil end
end
local function proxy_lib(libname)
  return setmetatable({}, { __index = function(_, k) return stub(libname .. "." .. k) end })
end

-- dump any sizable binary argument (shellcode / URLs / paths) to its own file
local dump_n = 0
local function dump_blob(a)
  if type(a) == "string" and #a > 16 then
    dump_n = dump_n + 1
    local p = string.format("blob.%02d.bin", dump_n)
    local cf = io.open(p, "wb"); cf:write(a); cf:close()
    rec("BLOB", "->" .. p, #a .. "B")
  end
end

-- universal permissive proxy: indexes, calls, concats, never returns nil,
-- so the payload's pointer/handle chains keep flowing and reveal the next call.
local function uproxy(label)
  return setmetatable({}, {
    __index    = function(_, k) return uproxy(label .. "." .. tostring(k)) end,
    __call     = function(_, ...)
      rec("ffi.call", label, ...)
      for i = 1, select("#", ...) do dump_blob((select(i, ...))) end
      return uproxy(label .. "()")
    end,
    __concat   = function() return "" end,
    __add = function() return 0 end, __sub = function() return 0 end,
    __tostring = function() return label end,
  })
end

local fake_ffi = setmetatable({
  os = "Windows", arch = "x64",
  load    = function(n) rec("ffi.load", n); return uproxy("lib:" .. tostring(n)) end,
  cdef    = function(d) rec("ffi.cdef", #d .. "B"); local cf = io.open("cdef.txt", "a"); cf:write(d .. "\n"); cf:close() end,
  C       = uproxy("C"),
  cast    = function(t, ...) rec("ffi.cast", t); for i = 1, select("#", ...) do dump_blob((select(i, ...))) end; return uproxy("cast") end,
  new     = function(t, ...) rec("ffi.new", t, ...); return uproxy("new") end,
  typeof  = function(t) rec("ffi.typeof", t); return uproxy("ctype") end,
  sizeof  = function() return 0 end,
  gc      = function(o) return o end,
  copy    = function(dst, src, n) rec("ffi.copy", n); dump_blob(src); return nil end,
  fill    = function() return nil end,
  string  = function(...) rec("ffi.string", ...); return "" end,
  abi     = function() return false end,
}, { __index = function(_, k) return stub("ffi." .. k) end })

local env = {}
env.string, env.table, env.math = string, table, math
env.tostring, env.tonumber = tostring, tonumber
env.pairs, env.ipairs, env.next = pairs, ipairs, next
env.select, env.type, env.error, env.assert = select, type, error, assert
env.pcall, env.xpcall, env.unpack = pcall, xpcall, unpack
env.rawget, env.rawset, env.rawequal = rawget, rawset, rawequal
env.setmetatable, env.getmetatable, env.newproxy = setmetatable, getmetatable, newproxy
env.print = function(...) rec("print", ...) end

env.os, env.io = proxy_lib("os"), proxy_lib("io")
env.loadstring = capture_chunk
env.load = capture_chunk
env.loadfile = function(p) rec("loadfile", p); return capture_chunk("") end
env.dofile = function(p) rec("dofile", p) end
local real_bit = require("bit")
env.require = function(m)
  rec("require", m)
  if m == "ffi" then return fake_ffi end
  if m == "bit" then return real_bit end
  return proxy_lib("require:" .. tostring(m))
end
env.collectgarbage = function() end
env.getfenv = function() return env end
env.setfenv = function(fn) return fn end
env._G, env._ENV = env, env

setmetatable(env, { __index = function(_, k) rec("GET", k); return nil end })

local chunk = assert(loadstring(src, "@uix.txt"))
setfenv(chunk, env)

rec("RUN_BEGIN")
local ok, err = pcall(chunk)
rec("RUN_END", ok, err)
io.write("done — see deob.log and any stage2.*.lua\n")
