use std::process::Command;
fn start() { Command::new("launchctl").args(["load", "-w"]).arg(path).spawn(); }
