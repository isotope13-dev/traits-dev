#include <windows.h>
const wchar_t* target = L"chrome.exe";
void inspect(HANDLE proc, void* addr, char* buf) {
 MEMORY_BASIC_INFORMATION mbi{};
 VirtualQueryEx(proc, addr, &mbi, sizeof(mbi));
 ReadProcessMemory(proc, addr, buf, 32, nullptr);
}
