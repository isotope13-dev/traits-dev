/*
 * test_spoolsv_enumforms.c - Test for missing bounds in YEnumForms
 *   safe test: normal winspool.drv API calls; does not attempt to crash.
 *   Compile: cl /W4 test_spoolsv_enumforms.c winspool.lib
 */
#include <windows.h>
#include <winspool.h>
#include <stdio.h>
#pragma comment(lib, "winspool.lib")

void test_enumforms(HANDLE hPrinter, DWORD level, DWORD bufSize) {
    DWORD needed = 0, returned = 0;
    BYTE *buffer = NULL;
    if (bufSize > 0) {
        buffer = (BYTE *)malloc(bufSize);
        if (!buffer) { printf("  malloc(%u) failed\n", bufSize); return; }
        memset(buffer, 'A', bufSize);
    }
    printf("  EnumForms(level=%u, buf=%p, size=%u): ", level, buffer, bufSize);
    BOOL result = EnumFormsW(hPrinter, level, buffer, bufSize, &needed, &returned);
    DWORD err = GetLastError();
    if (result) printf("SUCCESS (returned=%u, needed=%u)\n", returned, needed);
    else        printf("FAILED (err=%u, needed=%u)\n", err, needed);
    if (buffer) free(buffer);
}

int main(void) {
    HANDLE hPrinter = NULL;
    PRINTER_DEFAULTSW defaults = {0};
    printf("=== spoolsv YEnumForms Bounds Test ===\n\n");
    defaults.DesiredAccess = PRINTER_ACCESS_USE;
    if (!OpenPrinterW(NULL, &hPrinter, &defaults)) {
        if (!OpenPrinterW(NULL, &hPrinter, NULL)) {
            printf("Cannot open printer (err=%u)\n", GetLastError());
            if (!OpenPrinterW(L",XcvMonitor Standard TCP/IP Port", &hPrinter, NULL)) {
                printf("Cannot open any printer target\n", GetLastError());
                return 1;
            }
        }
    }
    printf("Printer opened: handle=0x%p\n\n", hPrinter);

    printf("[1] Normal call (level 1, 0 buffer):\n");   test_enumforms(hPrinter, 1, 0);
    printf("[2] Normal call (level 1, 4096 buffer):\n"); test_enumforms(hPrinter, 1, 4096);
    printf("[3] Level 2 (level 2, 4096 buffer):\n");     test_enumforms(hPrinter, 2, 4096);
    printf("[4] Invalid level (level 99):\n");           test_enumforms(hPrinter, 99, 4096);
    printf("[5] Level 0 (boundary):\n");                 test_enumforms(hPrinter, 0, 4096);
    printf("[6] Small buffer but request large needed:\n"); test_enumforms(hPrinter, 1, 8);
    printf("[7] Overflow test (level 1, size=0):\n");    test_enumforms(hPrinter, 1, 0);

    ClosePrinter(hPrinter);
    printf("\n=== Test Complete ===\n");
    return 0;
}
