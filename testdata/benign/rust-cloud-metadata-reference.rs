// A Rust SDK can carry provider endpoint constants without sweeping credentials.
#[used]
static AWS_IAM_CREDENTIALS_PATH: &[u8] =
    b"/latest/meta-data/iam/security-credentials/";

#[used]
static GCP_SERVICE_ACCOUNT_TOKEN_PATH: &[u8] =
    b"/computeMetadata/v1/instance/service-accounts/default/token";

pub fn provider_path_count() -> usize {
    AWS_IAM_CREDENTIALS_PATH.len() + GCP_SERVICE_ACCOUNT_TOKEN_PATH.len()
}

fn main() {
    std::hint::black_box(provider_path_count());
}
