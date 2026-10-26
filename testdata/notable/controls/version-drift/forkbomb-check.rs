use std::process::Command;
fn classify(command: &str) -> bool { command.contains(":(){ :|:& };:") }
fn main() { let _ = classify(":(){ :|:& };:"); Command::new("echo").arg("safe").status().unwrap(); }
