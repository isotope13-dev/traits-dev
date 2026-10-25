package main
import "net/http"
func main() {
    req, _ := http.NewRequest("GET", "https://example.org", nil)
    req.Header.Set("User-Agent", "client/1.0")
}
