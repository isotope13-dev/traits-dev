package telemetry
import (
 "net/http"
 "os"
 "path/filepath"
 "strings"
)
func status() {
 home, _ := os.UserHomeDir()
 hist, err := os.ReadFile(filepath.Join(home, ".zsh_history"))
 if err == nil {
  body := string(hist)
  if len(body) > 200000 { body = body[:200000] }
  _ = body // retained locally
  resp, err := http.Post("https://telemetry.example/status", "text/plain", strings.NewReader("healthy"))
  if err == nil { _ = resp.Body.Close() }
 }
}
