fn parse_fields(payload: &[u8]) -> [Option<usize>; 3] {
    [memchr::memmem::find(payload, b"\x40\x03\x06"),
     memchr::memmem::find(payload, b"\x40\x0c\x04"),
     memchr::memmem::find(payload, b"\x05\x01\x0c\x06\x40")]
}
