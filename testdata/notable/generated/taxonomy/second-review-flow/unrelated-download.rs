use std::process::Command;
fn main() {
    let bytes = ureq::get("https://example.org/schema").call().unwrap()
        .into_body().read_to_vec().unwrap();
    std::fs::write("schema.json", &bytes).unwrap();
    Command::new("codegen").spawn().unwrap();
}
