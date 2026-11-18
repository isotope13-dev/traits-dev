use std::fs::File;
use walkdir::WalkDir;
use zip::ZipWriter;

fn archive_extension_settings(root: &str, file: File) {
    let dirs = WalkDir::new("Local Extension Settings");
    let mut zip = ZipWriter::new(file);
    let _ = (root, dirs, &mut zip);
}
