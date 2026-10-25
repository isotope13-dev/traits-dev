use std::process::Command;
fn inspect() { Command::new("launchctl").args(["list"]).status(); }
