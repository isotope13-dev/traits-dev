// Inert analysis fixture. Never execute. Import signatures are scaffolding.
__declspec(dllimport) void HeapFree(void);
__declspec(dllimport) void SystemFunction033(void);
volatile unsigned hash_marker = 0xec0e4e8e;
void entry(void) { HeapFree(); SystemFunction033(); }
