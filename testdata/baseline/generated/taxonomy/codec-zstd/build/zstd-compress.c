__declspec(dllimport) void ZSTD_compress(void);
void entry(void) { ZSTD_compress(); }
