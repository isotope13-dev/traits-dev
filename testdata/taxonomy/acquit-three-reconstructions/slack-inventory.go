package main
import("bytes"; "encoding/json"; "fmt"; "net/http"; "os"; "os/exec"; "os/user"; "runtime")
// Explicitly configured inventory notifier; no remote execution.
func checkin(token string) {
    node, _ := exec.LookPath("node")
    host, _ := os.Hostname()
    u, _ := user.Current()
    data, _ := json.Marshal(map[string]string{
        "channel": "frontend-devs",
        "text": fmt.Sprintf("%s %s %s %s %s %s", runtime.GOOS, runtime.GOARCH, host, u.Username, u.HomeDir, node),
    })
    req, _ := http.NewRequest("POST", "https://slack.com/api/chat.postMessage", bytes.NewReader(data))
    req.Header.Set("Authorization", "Bearer "+token)
    resp, err := http.DefaultClient.Do(req)
    if err == nil { resp.Body.Close() }
}

func main(){checkin(os.Getenv("SLACK_TOKEN"))}
