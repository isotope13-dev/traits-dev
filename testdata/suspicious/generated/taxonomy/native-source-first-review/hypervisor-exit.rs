fn screening() { unsafe {
    let present = (__cpuid(1).ecx & (1 << 31)) != 0;
    _mm_clflush(std::ptr::null());
    let before = _rdtsc();
    let after = _rdtsc();
    if present || after < before { std::process::exit(0); }
}}
