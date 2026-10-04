// Inert analysis fixture. Never execute. Import signatures are scaffolding.
__declspec(dllimport) void HeapFree(void);
__declspec(dllimport) void LocalFree(void);
__declspec(dllimport) void capCreateCaptureWindowA(void);
__declspec(dllimport) void MAPIFreeBuffer(void);
void entry(void) { HeapFree(); LocalFree(); capCreateCaptureWindowA(); MAPIFreeBuffer(); }
