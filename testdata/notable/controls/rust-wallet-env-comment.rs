use std::env;
fn main() {
    // env::var("POLYMARKET_PRIVATE_KEY") is an example, not a read.
    let _ = env::var("RELAYER_URL");
}
