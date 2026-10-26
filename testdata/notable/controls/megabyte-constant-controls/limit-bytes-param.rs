//! Log tailing options.
// See https://github.com/kubernetes/kubernetes for the API conventions.
pub struct LogOptions {
    pub limit_bytes: Option<u64>,
}
/// Default: ten megabytes.
pub const DEFAULT_LIMIT: u64 = 10 * 1024 * 1024;
#[test]
fn limit_query() {
    assert_eq!("limitBytes=10485760", "limitBytes=10485760");
}
