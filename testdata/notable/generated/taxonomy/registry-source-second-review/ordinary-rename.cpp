void move(HANDLE h, FILE_RENAME_INFO *info) { const wchar_t *s=L":stream"; SetFileInformationByHandle(h, FileRenameInfo, info, sizeof(*info)); }
