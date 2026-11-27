package main
import ("net/http"; "io"; "os")
func unrelated(f *os.File) {
http.Get("https://example.com/next")
b, _ := io.ReadAll(f)
http.Post(string(b), "application/json", nil)
}
