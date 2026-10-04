__declspec(dllimport) void *VirtualAllocEx(void *, void *, unsigned long long, unsigned, unsigned); void *entry(void) { return VirtualAllocEx((void *)1, 0, 4096, 0x1000, 4); }
