// A social client validates signed encrypted messages without a shell.
const RELAYS: &str = "https://api.nostr.watch/v1/online";
const ERRORS: [&str; 4] = ["No website found in metadata", "Failed to decode base64 encrypted data", "Failed to decode base64 signature data", "Unknown command type: "];
fn main() { println!("{} {}", RELAYS, ERRORS[0]); }
