package main
import (h "net/http"; "io")
func route() {
r, _ := h.Get("https://example.com/next")
b, _ := io.ReadAll(r.Body)
h.Post(string(b), "application/json", nil)
}
