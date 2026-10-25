#include <windows.h>
void probe(HANDLE destination, void *path, LPTHREAD_START_ROUTINE worker) {
  auto unused = GetProcAddress(GetModuleHandleA("kernel32.dll"), "LoadLibraryW");
  CreateRemoteThread(destination, nullptr, 0, worker, path, 0, nullptr);
}
