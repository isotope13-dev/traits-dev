// Positive: dd named as a spawned child-process command.
pub fn zero_fill(device: &str) {
    let _ = std::process::Command::new("dd")
        .arg("if=/dev/zero")
        .arg(format!("of={device}"))
        .status();
}
