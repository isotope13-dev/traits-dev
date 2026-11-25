package replaycapture

import "testing"

func TestLinterRejectsIMDS(t *testing.T) {
	cases := []string{
		`"target": "http://169.254.169.254/latest/meta-data/"`,
	}
	for _, c := range cases {
		if !lintRejects(c) {
			t.Fatalf("expected rejection for %s", c)
		}
	}
}
