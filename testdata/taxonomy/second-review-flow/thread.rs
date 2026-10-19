use std::process::Command;
fn main() {
    let _unstarted = Command::new("builder");
    std::thread::Builder::new().spawn(|| {}).unwrap();
}
