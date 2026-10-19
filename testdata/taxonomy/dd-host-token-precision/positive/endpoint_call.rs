// Positive: an endpoint name bound from a discovery call.
fn discover_endpoint() -> &'static str {
    "https://api.example.test/v1"
}

pub fn connect() {
    let endpoint = discover_endpoint();
    println!("connecting: {endpoint}");
}
