use std::process::Command;
fn main() {
    let mut helper = Command::new("builder");
    helper.arg("--version");
    helper.spawn().unwrap();
}
