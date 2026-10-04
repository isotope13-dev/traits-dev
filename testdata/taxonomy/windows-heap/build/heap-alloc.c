// Inert static-analysis fixture; never execute. Signature is import scaffolding.
__declspec(dllimport) void HeapAlloc(void);
void entry(void) { HeapAlloc(); }
