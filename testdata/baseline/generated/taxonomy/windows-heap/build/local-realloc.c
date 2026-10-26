// Inert static-analysis fixture; never execute. Signature is import scaffolding.
__declspec(dllimport) void LocalReAlloc(void);
void entry(void) { LocalReAlloc(); }
