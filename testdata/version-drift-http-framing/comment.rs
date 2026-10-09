// An empty body (`Content-Length: 0`) is sent as zero length.
// reqwest emits `Content-Length: 0`, rather than chunked encoding.
fn main() {}
