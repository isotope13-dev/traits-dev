package example
import "net/http/httptest"
var factory = httptest.NewServer
var message = "httptest.NewServer(handler)"
func makeServer() { _ = httptest.NewUnstartedServer(nil) }
