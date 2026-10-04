__declspec(dllimport) void *memcpy(void *, const void *, unsigned long long); void *entry(void) { return memcpy((void *)1, (void *)2, 48); }
