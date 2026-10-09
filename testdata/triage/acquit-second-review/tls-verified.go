package probe
import "crypto/tls"
// InsecureSkipVerify: true
var config = &tls.Config{InsecureSkipVerify: false}
