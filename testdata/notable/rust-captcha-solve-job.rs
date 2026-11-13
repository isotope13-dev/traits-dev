// Positive fixture: a CAPTCHA-solving client job schema. The site-key and
// page-URL fields together are the solver-input schema; the page field uses
// snake_case, so the page-input leg must still feed the composite even
// though the bare field name alone is generic web vocabulary.
#[derive(Default)]
pub struct SolveJob {
    pub sitekey: String,
    pub page_url: String,
    pub pageaction: Option<String>,
}

impl SolveJob {
    pub fn new(sitekey: &str, page_url: &str) -> Self {
        Self {
            sitekey: sitekey.to_string(),
            page_url: page_url.to_string(),
            pageaction: None,
        }
    }

    pub fn to_payload(&self) -> String {
        format!("?key={}&sitekey={}&pageurl={}", "api-key", self.sitekey, self.page_url)
    }
}
