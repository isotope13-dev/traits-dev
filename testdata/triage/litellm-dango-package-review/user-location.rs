// Request configuration from the actual web-search serialization test.
fn request() {
    let _tool = serde_json::json!({"type":"web_search_20250305", "name":"web_search",
        "user_location":{"type":"approximate", "city":"San Francisco", "country":"US"}});
}
