// Benign macOS LaunchAgent installer for a third-party desktop sync helper.
package launchagent

import (
	"os"
	"os/exec"
	"path/filepath"
)

func InstallSyncAgent(home string, binPath string) error {
	plistPath := filepath.Join(home, "Library", "LaunchAgents", "io.example.filesync.plist")
	plist := `<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0"><dict>
  <key>Label</key><string>io.example.filesync</string>
  <key>ProgramArguments</key><array><string>` + binPath + `</string></array>
  <key>RunAtLoad</key><true/>
</dict></plist>`
	if err := os.WriteFile(plistPath, []byte(plist), 0o644); err != nil {
		return err
	}
	return exec.Command("launchctl", "load", plistPath).Run()
}
