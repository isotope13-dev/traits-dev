#include <windows.h>
void inject(HANDLE destination, void *path) {
  LPTHREAD_START_ROUTINE entry = (LPTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandleA("kernel32.dll"), "LoadLibraryW");
  CreateRemoteThread(destination, nullptr, 0, entry, path, 0, nullptr);
}
