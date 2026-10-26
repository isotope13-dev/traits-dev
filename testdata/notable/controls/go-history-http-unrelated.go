// The helper is called twice; the upload uses only the public fixture.
package historyfixture

import (
	"bytes"
	"net/http"
	"os"
	"path/filepath"
)

func fixtureBytes(path string) []byte {
	data, _ := os.ReadFile(path)
	return data
}

func uploadPublicFixture() {
	history := fixtureBytes(filepath.Join("/tmp/history-fixture", ".zsh_history"))
	_ = len(history)
	public := fixtureBytes(filepath.Join("/tmp/history-fixture", "public.txt"))
	http.Post("https://history-fixture.invalid/upload", "text/plain", bytes.NewReader(public))
}
