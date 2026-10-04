pub unsafe fn mapping() { let prot = libc::PROT_READ | libc::PROT_EXEC; let p = libc::mmap(0, 4096, prot, 0, -1, 0); }
