package proxy

import "net/http"

// Probe helper with no test harness or integration tag: the normalization
// payload is shipped code, so it must keep firing.
func BuildProbe(host string) (*http.Request, error) {
	return http.NewRequest(http.MethodGet, "http://"+host+"/test/..;/..;/admin", nil)
}
