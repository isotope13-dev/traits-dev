void probe(void) { GetNativeSystemInfo(&si); GlobalMemoryStatusEx(&m); if (m.ullTotalPhys < 2147483648ULL) fallback(); GetSystemMetrics(0); }
