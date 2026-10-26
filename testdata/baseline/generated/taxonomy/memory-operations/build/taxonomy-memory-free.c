__declspec(dllimport) void free(void *); void entry(void) { free((void *)1); }
