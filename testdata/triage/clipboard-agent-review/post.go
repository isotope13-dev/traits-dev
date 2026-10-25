package main
import "net/http"
func main() { http.Post("https://example.org/status", "text/plain", nil) }
