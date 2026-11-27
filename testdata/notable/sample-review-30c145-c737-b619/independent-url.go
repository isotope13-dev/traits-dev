package main
import ("net/http"; "net/url")
func independent(u url.URL) {
http.Get(u.String())
http.Post(u.String(), "application/json", nil)
}
