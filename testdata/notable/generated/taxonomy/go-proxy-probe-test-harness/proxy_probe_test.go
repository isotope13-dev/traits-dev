package proxy

import (
	"net/http"
	"testing"
)

func TestBuildProbe(t *testing.T) {
	r, _ := http.NewRequest(http.MethodGet, "http://127.0.0.1/test/..;/..;/admin", nil)
	if r.URL.Path == "" {
		t.Fatal("empty path")
	}
}
