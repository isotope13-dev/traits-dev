// Allocates a scratch page through Koffi for a native image decoder.
const koffi = require('koffi');
const k32 = koffi.load('kernel32.dll');
const VirtualAlloc = k32.func('void* VirtualAlloc(void* lpAddress, size_t dwSize, uint32_t flAllocationType, uint32_t flProtect)');
const VirtualFree = k32.func('int VirtualFree(void* lpAddress, size_t dwSize, uint32_t dwFreeType)');
const page = VirtualAlloc(null, 65536, 0x3000, 0x04);
VirtualFree(page, 0, 0x8000);
module.exports = { page };
