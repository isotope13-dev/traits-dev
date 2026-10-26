local function log(level, message)
    io.stderr:write(string.format("[%s] %s\n", level, message))
end

log("info", "this sample does nothing")
