#include <windows.h>
constexpr ULONG ProcessDebugFlags = 31;
constexpr ULONG ThreadHideFromDebugger = 17;
NTSTATUS NtQueryInformationProcess(HANDLE process, ULONG infoClass, void *buffer,
                                  ULONG length, ULONG *returned);
NTSTATUS NtSetInformationThread(HANDLE thread, ULONG infoClass, void *buffer, ULONG length);
const char *queryExample = "NtQueryInformationProcess(process, 31, buffer, 4, nullptr)";
// NtSetInformationThread(thread, 17, nullptr, 0)
void inspect(HANDLE process, HANDLE thread) {
    NtQueryInformationProcess(process, 0, nullptr, 31, nullptr);
    NtSetInformationThread(thread, 0, nullptr, 17);
}
