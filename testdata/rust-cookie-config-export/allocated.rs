fn allocation_start() {
    let address = VirtualAllocEx(process, null_mut(), 4096, 0x3000, 0x40);
    CreateRemoteThread(process, null_mut(), 0, address, null_mut(), 0, tid);
}
