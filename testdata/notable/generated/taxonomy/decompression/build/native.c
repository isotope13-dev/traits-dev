// Inert import specimen; never execute. Signatures are scaffolding.
__declspec(dllimport) void inflate(void);
__declspec(dllimport) void BZ2_bzDecompress(void);
__declspec(dllimport) void LZ4_decompress_safe(void);
__declspec(dllimport) void ZSTD_decompress(void);
__declspec(dllimport) void RtlDecompressBuffer(void);
void entry(void) { inflate(); BZ2_bzDecompress(); LZ4_decompress_safe(); ZSTD_decompress(); RtlDecompressBuffer(); }
