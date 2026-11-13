// Benign control: MCP server descriptor carrying a `website_url` field.
// The field name matches CAPTCHA-solver page-URL vocabulary, but with no
// site-key schema beside it there is no solver job, so no CAPTCHA input
// finding may fire on this file.
#[derive(Debug, Default)]
pub struct ServerInfo {
    pub server_name: String,
    pub server_version: String,
    pub website_url: Option<String>,
    pub instructions: Option<String>,
}

pub fn server_descriptor() -> ServerInfo {
    ServerInfo {
        server_name: "kreuzberg-mcp".to_string(),
        server_version: "4.10.4".to_string(),
        website_url: Some("https://kreuzberg-dev.github.io/kreuzberg/".to_string()),
        instructions: Some("Document extraction toolkit".to_string()),
    }
}

pub fn with_website_url(mut info: ServerInfo, url: &str) -> ServerInfo {
    info.website_url = Some(url.to_string());
    info
}
