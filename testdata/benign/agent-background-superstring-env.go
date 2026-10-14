// Benign control: an env-var namespace that merely contains the ART-C2
// background-command token as a substring of a longer identifier. An
// identifier-anchored source match must not fire here; only the bare
// protocol token is the marker.
package gateway

import "os"

func backgroundMode() string {
	if v := os.Getenv("MYAPP_AGENT_BACKGROUND"); v != "" {
		return v
	}
	return "auto"
}

func agentEnv() map[string]string {
	return map[string]string{
		"bin":     os.Getenv("MYAPP_AGENT_BIN"),
		"image":   os.Getenv("MYAPP_AGENT_CONTAINER_IMAGE"),
		"manager": os.Getenv("MYAPP_AGENT_SERVICE_MANAGER"),
		"name":    os.Getenv("MYAPP_AGENT_SERVICE_NAME"),
		"state":   os.Getenv("MYAPP_AGENT_STATE_DIR"),
		"cache":   os.Getenv("MYAPP_AGENT_CACHE_DIR"),
		"exec":    os.Getenv("MYAPP_AGENT_EXECUTOR"),
	}
}
