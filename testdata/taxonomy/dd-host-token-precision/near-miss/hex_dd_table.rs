// Near miss: "dd" here is a hex digit in a lookup table, not the disk tool.
const HEX_DIGITS: &[&str] = &["d0", "d1", "da", "db", "dc", "dd", "de", "df"];

pub fn hex_name(nibble: u8) -> &'static str {
    HEX_DIGITS[(nibble & 0xf) as usize]
}
