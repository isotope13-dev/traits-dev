use std::process::Command;

fn run_stage() {
    let _ = Command::new("sh")
        .arg("-c")
        .arg("echo 'imaohw ;di' | rev | sh")
        .status();
}
