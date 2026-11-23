use std::fs;
use std::os::unix::fs::PermissionsExt;
fn prepare_tool() -> std::io::Result<()> {
    fs::set_permissions("local-tool", fs::Permissions::from_mode(0o755))
}
