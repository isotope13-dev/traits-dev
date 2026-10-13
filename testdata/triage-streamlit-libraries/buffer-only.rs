use std::io::Write;
pub fn write_data(writer: &mut impl Write, buf: &[u8]) {
    writer.write_all(buf).unwrap();
}
