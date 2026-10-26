// Inert static-analysis fixture; never execute. Signature is import scaffolding.
__declspec(dllimport) void HeapReAlloc(void);
void entry(void) { HeapReAlloc(); }
