// Near miss: host_arch is CPU architecture, not a network host.
fn host_arch() -> &'static str {
    "x86_64"
}

pub fn describe() {
    let host_arch_value = host_arch();
    let host_name = host_arch_to_string(host_arch_value);
    println!("host architecture: {host_arch_value} ({host_name})");
}
