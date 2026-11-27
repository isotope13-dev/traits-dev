#include <windows.h>
void f(void) { void *p=VirtualAlloc(0,4096,MEM_COMMIT,PAGE_READWRITE); DWORD old; VirtualProtect(p,4096,PAGE_EXECUTE_READ,&old); EnumDesktopsA(GetProcessWindowStation(), visit, 0); }
