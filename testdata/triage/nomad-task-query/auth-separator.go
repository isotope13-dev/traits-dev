package api
import "strings"
func split(auth string) bool { return strings.Contains(auth, ":") }
