// Inert static-analysis fixture; never execute. Signature is import scaffolding.
__declspec(dllimport) void HeapFree(void);
void entry(void) { HeapFree(); }
