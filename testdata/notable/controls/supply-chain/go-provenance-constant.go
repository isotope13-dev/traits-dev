package sample
import ("net/http"; "os"; "strings")
func identity(value string) string { return value }
func run() {
    identity(os.Getenv("DEPLOY_API_KEY"))
    http.Post("https://collector.invalid", "text/plain", strings.NewReader(identity("status")))
}
