const MIME_TYPES: &[&str] = &["text/plain"];
struct Request { body: Option<String> }
fn mode() -> &'static str { "--headless" }
