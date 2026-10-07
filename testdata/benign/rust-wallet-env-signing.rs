use std::env;
fn main() {
    let key = env::var("POLYMARKET_PRIVATE_KEY").unwrap();
    let signer = key.parse::<PrivateKeySigner>().unwrap();
    println!("{}", signer.address());
}
