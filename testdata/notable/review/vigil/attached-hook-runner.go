package hooks

import (
	"encoding/base64"
	"os"
	"os/exec"
	"path/filepath"
)

// RunHook writes a user-supplied Base64 hook script and runs it attached,
// so its output and exit status reach the operator.
func RunHook(dir, b64 string) error {
	raw, err := base64.StdEncoding.DecodeString(b64)
	if err != nil {
		return err
	}
	path := filepath.Join(dir, "hook.sh")
	if err := os.WriteFile(path, raw, 0o700); err != nil {
		return err
	}
	cmd := exec.Command("/bin/sh", path)
	cmd.Stdout, cmd.Stderr = os.Stdout, os.Stderr
	return cmd.Run()
}
