package logging

import "testing"

func TestFormat(t *testing.T) {
	if got := format("x"); got != "x" {
		t.Fatal(got)
	}
}
