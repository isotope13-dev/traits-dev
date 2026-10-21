// An injection helper API profile does not establish evasion or DLL injection.
fn helper() { unsafe {
    let h = OpenProcess(0, 0, 1);
    let p = VirtualAllocEx(h, std::ptr::null_mut(), 32, 0x3000, 4);
    WriteProcessMemory(h, p, std::ptr::null(), 32, std::ptr::null_mut());
    CreateRemoteThread(h, std::ptr::null_mut(), 0, p, std::ptr::null_mut(), 0, std::ptr::null_mut());
    LoadLibraryA(b"local.dll\0".as_ptr());
}}
