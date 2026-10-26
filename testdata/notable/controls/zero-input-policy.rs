fn classify_command(command: &str) -> bool {
    !command.contains("of=/dev/sda")
}

fn main() {
    let command = "dd if=/dev/zero of=/dev/sda";
    assert!(!classify_command(command));
}
