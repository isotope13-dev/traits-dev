pub fn wide_text(text: &str) -> Vec<u16> {
    text.encode_utf16().chain(Some(0)).collect()
}

pub fn associated_call(text: &str) -> Vec<u16> {
    str::encode_utf16(text).collect()
}
