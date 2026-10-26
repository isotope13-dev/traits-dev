// Dependency-fetch build script with toolchain discovery only: it
// downloads a client binary over HTTP and writes it out, but the only
// child process it launches is `python -c` for interpreter discovery
// (.output(), never .spawn()). Fetch plus construction is not fetch plus
// execution, so build-rs-fetches-and-runs-payload stays silent here.
use std::process::Command;

fn main() {
    let resp = ureq::get("https://pypi.org/pypi/pkg/1.0/json").call().unwrap();
    let body = resp.into_body().read_to_vec().unwrap();
    std::fs::write("out.bin", &body).unwrap();
    let py = std::env::var_os("PYO3_PYTHON").unwrap();
    let _ = Command::new(&py)
        .args(["-c", "import sys; print(sys.base_prefix)"])
        .output()
        .unwrap();
}
