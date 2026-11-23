use std::fs;
use std::os::unix::fs::PermissionsExt;
fn protect_config() -> std::io::Result<()> {
    fs::set_permissions("settings.conf", fs::Permissions::from_mode(0o600))
}
