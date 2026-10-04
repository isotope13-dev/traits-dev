__declspec(dllimport) void *realloc(void *, unsigned long long); void *entry(void) { return realloc((void *)1, 48); }
