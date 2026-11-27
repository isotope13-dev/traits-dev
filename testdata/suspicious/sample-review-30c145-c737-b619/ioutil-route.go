package main
import ("net/http"; "io/ioutil")
func route() {
r, _ := http.Get("https://example.com/next")
b, _ := ioutil.ReadAll(r.Body)
http.Post(string(b), "application/json", nil)
}
