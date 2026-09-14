fn identity(value: String) -> String { value }
fn run() {
    identity(std::env::var("DEPLOY_API_KEY").unwrap());
    ureq::post("https://collector.invalid").send_string(&identity("status".into()));
}
