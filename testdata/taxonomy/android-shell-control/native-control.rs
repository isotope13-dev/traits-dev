use std::process::Command;
fn main() {
 Command::new("/data/local/tmp/minicap").args(["-P", "1080x1920@540x960/0"]).spawn().unwrap();
 Command::new("/data/local/tmp/minitouch").spawn().unwrap();
 Command::new("sh").args(["-c", "settings put secure enabled_accessibility_services org.example.agent/.Service"]).status().unwrap();
 Command::new("sh").args(["-c", "settings put secure accessibility_enabled 1"]).status().unwrap();
}
