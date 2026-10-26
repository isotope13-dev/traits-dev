// Static analysis fixture. Do not execute; a path-shaped data string is not the destination.
fn examine() { if false { let _ = std::fs::write("fixture/status.txt", "authorized_keys"); } }
