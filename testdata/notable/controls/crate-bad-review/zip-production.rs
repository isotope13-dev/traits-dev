use zip::ZipWriter;
fn archive(output: &mut std::io::Cursor<Vec<u8>>) {
    let mut writer = ZipWriter::new(output);
    writer.start_file("entry", zip::write::SimpleFileOptions::default());
}
