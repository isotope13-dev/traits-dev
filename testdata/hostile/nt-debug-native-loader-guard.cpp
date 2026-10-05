#include <windows.h>
#include <winternl.h>

using NtQueryInformationProcessFn = NTSTATUS (NTAPI *)(HANDLE, ULONG, PVOID, ULONG, PULONG);
using NtSetInformationThreadFn = NTSTATUS (NTAPI *)(HANDLE, ULONG, PVOID, ULONG);
constexpr ULONG ProcessDebugFlags = 31;
constexpr ULONG ThreadHideFromDebugger = 17;

bool prepare_loader() {
    HMODULE ntdll = GetModuleHandleW(L"ntdll.dll");
    auto NtQueryInformationProcess = reinterpret_cast<NtQueryInformationProcessFn>(
        GetProcAddress(ntdll, "NtQueryInformationProcess"));
    auto NtSetInformationThread = reinterpret_cast<NtSetInformationThreadFn>(
        GetProcAddress(ntdll, "NtSetInformationThread"));
    if (!NtQueryInformationProcess || !NtSetInformationThread) return false;
    ULONG flags = 0;
    if (NtQueryInformationProcess(GetCurrentProcess(), ProcessDebugFlags,
                                  &flags, sizeof(flags), nullptr) < 0 || flags == 0)
        return false;
    return NtSetInformationThread(GetCurrentThread(), ThreadHideFromDebugger,
                                  nullptr, 0) >= 0;
}
