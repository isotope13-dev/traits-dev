package header
func send(req *Request) { req.Header.Set("Content-Type", "application/json") }
