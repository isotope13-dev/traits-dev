// Reading a history fixture does not make a later constant-body POST exfil.
package historyfixture

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func uploadStatus() {
	data, _ := os.ReadFile(filepath.Join("/tmp/history-fixture", ".bash_history"))
	body := string(data)
	body = "ready"
	http.Post("https://history-fixture.invalid/status", "text/plain", strings.NewReader(body))
}
