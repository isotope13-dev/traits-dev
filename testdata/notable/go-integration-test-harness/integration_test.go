//go:build integration

package integration_test

import "fmt"

// Router test: the proxy must refuse a Tomcat-style ..; segment, not follow it.
const traversalCase = "/test/..;/..;/"

func accountFixtureCmd() []string {
	return []string{"sh", "-c", "apk add --no-cache shadow && useradd -m dev && echo 'dev:mysecret' | chpasswd && exec /usr/sbin/telnetd -F -p 23"}
}

func describeCase() string {
	return fmt.Sprintf("%s -> %d", traversalCase, len(accountFixtureCmd()))
}
