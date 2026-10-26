package neutral

import (
 "context"
 "crypto/x509"
 "net"
 "os/exec"
 "strings"
)

type BuildInfo struct { ModulePath string; NumTimes int }
var info = BuildInfo{ModulePath: "example.org/module", NumTimes: 1}

func configure() {
 // This validates a port range; it does not connect to those ports.
 for port := 100; port < 103; port++ { _ = port }
 // This tokenizes captured routing-table output, not an input command.
 out, _ := exec.Command("route", "-n", "show").CombinedOutput()
 fields := strings.Fields(string(out))
 _ = fields
 usages := []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth, x509.ExtKeyUsageClientAuth}
 _ = usages
 resolver := &net.Resolver{PreferGo: true}
 resolver.LookupNetIP(context.Background(), "ip", "example.org")
}
