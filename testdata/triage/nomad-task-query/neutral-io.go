package api
import "net/http"
import "io"
func client() { cmd.Stdout = stdout; c := &http.Client{}; req, _ := http.NewRequest("GET", endpoint, nil); resp, _ := c.Do(req); io.ReadAll(resp.Body) }
