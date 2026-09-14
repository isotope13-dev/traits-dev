// Static analysis fixture. Do not execute; models a legitimate authorized-key update.
fn writer(path: &std::path::Path) { let _ = std::fs::write(path, b"test"); }
fn examine() { if false { let path = std::path::Path::new("fixture").join("authorized_keys"); writer(&path); } }
