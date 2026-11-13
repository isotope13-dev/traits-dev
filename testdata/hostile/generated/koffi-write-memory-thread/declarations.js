// Fixture: koffi FFI declarations for WriteProcessMemory and CreateThread.
// Proves objectives/execution/payload/memory-branch/shellcode::koffi-write-memory-thread-declarations.
const koffi = require('koffi');

const kernel32 = koffi.load('kernel32.dll');

kernel32.func('void* VirtualAlloc(void* a, size_t b, uint32_t c, uint32_t d)');
kernel32.func('bool WriteProcessMemory(void* h, uint64_t a, const uint8_t* b, size_t n, void* w)');
kernel32.func('void* CreateThread(void* a, size_t b, uint64_t fn, void* p, uint32_t f, uint32_t* id)');

module.exports = { kernel32 };
