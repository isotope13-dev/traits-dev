#[tokio::test]
async fn rejects_a_smuggled_followup_request() {
    raw.send("POST /v1/files HTTP/1.1\r\nhost: x\r\ncontent-length: 3\r\ntransfer-encoding: chunked\r\n\r\n5\r\nhello\r\n0\r\n\r\nGET /next HTTP/1.1\r\nhost: x\r\n\r\n");
    assert_eq!(response.status(), StatusCode::BAD_REQUEST);
    assert!(received.try_recv().is_err());
}
