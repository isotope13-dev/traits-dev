use std::fs;
use std::io::Write;
pub fn write_data(buf: &[u8]) {
    let mut file = fs::File::create("data.bin").unwrap();
    file.write_all(buf).unwrap();
}
