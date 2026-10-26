// Inert static-analysis fixture; never execute. Signature is import scaffolding.
__declspec(dllimport) void LocalFree(void);
void entry(void) { LocalFree(); }
