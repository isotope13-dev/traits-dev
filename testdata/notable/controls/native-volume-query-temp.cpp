#include <windows.h>
#include <winternl.h>
void inspect(HANDLE volume, OBJECT_ATTRIBUTES* attrs) {
    FILE_FS_FULL_SIZE_INFORMATION size;
    IO_STATUS_BLOCK io;
    NtQueryVolumeInformationFile(volume, &io, &size, sizeof(size), FileFsFullSizeInformation);
    auto freeBytes = size.BytesPerSector * size.SectorsPerAllocationUnit * size.ActualAvailableAllocationUnits.QuadPart;
    HANDLE temporary;
    NtCreateFile(&temporary, GENERIC_WRITE | DELETE, attrs, &io, NULL,
        FILE_ATTRIBUTE_HIDDEN, FILE_SHARE_READ, FILE_CREATE, FILE_DELETE_ON_CLOSE, NULL, 0);
    CloseHandle(temporary);
}
