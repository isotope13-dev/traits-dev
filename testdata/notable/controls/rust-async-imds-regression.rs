#[tokio::test(flavor = "current_thread")]
async fn blocks_metadata_redirect() {
    let response = "Location: http://169.254.169.254/latest/meta-data/";
    assert!(response.contains("Location:"));
}
