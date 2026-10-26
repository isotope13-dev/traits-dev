#include <windows.h>
#include <winternl.h>
NTSTATUS map_local_image(HANDLE file, HANDLE *section, PVOID *base) {
    SIZE_T size = 0;
    NTSTATUS status = NtCreateSection(section, SECTION_ALL_ACCESS, NULL, NULL,
                                      PAGE_READONLY, SEC_IMAGE, file);
    if (status < 0) return status;
    return NtMapViewOfSection(*section, GetCurrentProcess(), base, 0, 0,
                             NULL, &size, 2, 0, PAGE_READONLY);
}
