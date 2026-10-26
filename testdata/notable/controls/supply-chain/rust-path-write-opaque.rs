// Static analysis fixture. Do not execute; external return values remain unknown.
fn examine() { if false { let _ = std::fs::write(opaque("authorized_keys"), b"test"); } }
