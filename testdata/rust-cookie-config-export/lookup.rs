fn resolve() {
    let result = unpack("arbitrary opaque text", 31, 7);
    let pointer = GetProcAddress(module, result.as_ptr());
}
