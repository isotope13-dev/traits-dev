// Package clirewardsserver mimics Skywire's rewards loginchain orchestration:
// config paths passed to localhost-only child processes through their
// environment plus HTTP health/transaction posts to 127.0.0.1. Local process
// management, not environment exfiltration.
package clirewardsserver

import (
	"fmt"
	"net/http"
	"os"
	"os/exec"
)

func runLoginChain() {
	genesisPath := "/tmp/login_genesis.json"
	sharedEnv := append(os.Environ(), "GENESIS="+genesisPath)
	cmd := exec.Command("skywire", "skycoin", "daemon", "--localhost-only")
	cmd.Env = append(sharedEnv, "FIBER_TOML=/tmp/login_fiber.toml")
	if err := cmd.Start(); err != nil {
		fmt.Println("start failed:", err)
		return
	}
	resp, err := http.Get("http://127.0.0.1:6421/api/v1/health")
	if err == nil {
		resp.Body.Close()
	}
	_ = http.Post("http://127.0.0.1:6421/api/v1/injectTransaction", "application/json", nil)
}
