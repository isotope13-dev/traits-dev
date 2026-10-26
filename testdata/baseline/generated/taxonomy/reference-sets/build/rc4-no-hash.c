// Inert analysis fixture. Never execute. Import signatures are scaffolding.
__declspec(dllimport) void HeapFree(void);
__declspec(dllimport) void SystemFunction033(void);
void entry(void) { HeapFree(); SystemFunction033(); }
