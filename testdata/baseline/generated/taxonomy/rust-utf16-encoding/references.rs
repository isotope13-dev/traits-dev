// text.encode_utf16().collect::<Vec<u16>>() is an example, not a call.
pub const EXAMPLE: &str = "str::encode_utf16(text)";

pub trait Encoder {
    fn encode_utf16(&self) -> Vec<u16>;
}

pub fn encode_utf16_description() -> &'static str {
    EXAMPLE
}
