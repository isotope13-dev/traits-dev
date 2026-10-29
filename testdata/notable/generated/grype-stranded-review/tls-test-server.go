package example
import "net/http/httptest"
func makeServer() { server := httptest.NewTLSServer(nil); defer server.Close() }
