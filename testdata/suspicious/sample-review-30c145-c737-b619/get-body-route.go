package main
import ("net/http"; "io")
func route() {
r, _ := http.Get("https://example.com/next")
b, _ := io.ReadAll(r.Body)
http.Post(string(b), "application/json", nil)
}
