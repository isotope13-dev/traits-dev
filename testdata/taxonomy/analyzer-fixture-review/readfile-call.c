void copy(HANDLE h, void *p, DWORD n, DWORD *out) { ReadFile(h, p, n, out, 0); }
