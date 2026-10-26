// Inert analysis fixture. Never execute. Import signatures are scaffolding.
__declspec(dllimport) void HeapAlloc(void);
__declspec(dllimport) void capCreateCaptureWindowA(void);
__declspec(dllimport) void MAPIFreeBuffer(void);
void entry(void) { HeapAlloc(); capCreateCaptureWindowA(); MAPIFreeBuffer(); }
