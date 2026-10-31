// github.com/Goldziher/basemind
const IMDS_PATH: &str = "/latest/meta-data/iam/security-credentials/";
const ENV_NAMES: &str = "AWS_SECRET_ACCESS_KEY AZURE_CLIENT_SECRET";
fn main() { println!("{} {}", IMDS_PATH, ENV_NAMES); }
