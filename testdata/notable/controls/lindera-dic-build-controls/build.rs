use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    use std::env;
    use std::fs::{rename, File};
    use std::io::{self, Write};
    use std::path::Path;

    use flate2::read::GzDecoder;
    use tar::Archive;

    println!("cargo:rerun-if-changed=build.rs");

    // Directory path for build package
    let build_dir = env::var_os("OUT_DIR").unwrap(); // ex) target/debug/build/<pkg>/out

    // Dictionary file name
    let file_name = "mecab-ko-dic-2.1.1-20180720.tar.gz";

    // Source file path for build package
    let source_path_for_build = Path::new(&build_dir).join(file_name);

    // Download source file to build directory
    if !source_path_for_build.exists() {
        let tmp_path = Path::new(&build_dir).join(file_name.to_owned() + ".download");

        // Download a tarball
        let download_url = "https://github.com/lindera-morphology/mecab-ko-dic/archive/refs/tags/2.1.1-20180720.tar.gz";
        let resp = ureq::get(download_url).call()?;
        let mut dest = File::create(&tmp_path)?;

        io::copy(&mut resp.into_reader(), &mut dest)?;
        dest.flush()?;

        rename(tmp_path, &source_path_for_build).expect("Failed to rename temporary file");
    }

    // Decompress a tar.gz file
    let tar_gz = File::open(source_path_for_build)?;
    let decoder = GzDecoder::new(tar_gz);
    let mut archive = Archive::new(decoder);
    archive.unpack(&build_dir)?;

    Ok(())
}
