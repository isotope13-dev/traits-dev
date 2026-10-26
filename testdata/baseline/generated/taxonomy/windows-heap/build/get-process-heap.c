// Inert static-analysis fixture; never execute. Signature is import scaffolding.
__declspec(dllimport) void GetProcessHeap(void);
void entry(void) { GetProcessHeap(); }
