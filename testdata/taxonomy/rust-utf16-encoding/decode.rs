pub fn read_wide(units: &[u16]) -> String {
    char::decode_utf16(units.iter().copied())
        .map(|unit| unit.unwrap_or(char::REPLACEMENT_CHARACTER))
        .collect()
}
