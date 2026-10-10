use std::process::Command;
use ed25519_dalek::SigningKey;
fn update(current_exe: &str, backup_path: &str, bytes: &[u8], args: &[String]) {
    std::fs::rename(&current_exe, &backup_path).unwrap();
    let _ = hex::encode(bytes);
    let _ = hex::decode("aabb");
    let _ = std::process::Command::new(current_exe).args(args).exec();
}
fn devices(device: &str) {
    let query = "SELECT * from Win32_PnPEntity";
    let _ = device.contains("microphone");
}
