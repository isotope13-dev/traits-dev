// Inert analysis fixture. Never execute. Import signatures are scaffolding.
__declspec(dllimport) void HeapFree(void);
void entry(void) { HeapFree(); }
