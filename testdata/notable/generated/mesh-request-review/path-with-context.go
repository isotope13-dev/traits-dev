package main
import "os"
var shell = "/bin/sh"
var command = "pm disable-user com.android.vending"
var encoded = []string{"🦀", "🦁", "🦂", "🦃", "🦄", "🦅", "🦆", "🦇", "🦈", "🦉", "🦊", "🦋", "🦌", "🦍", "🦎", "🦏", "🦐", "🦑", "🦒", "🦓", "🦔", "🦕", "🦖", "🦗"}
func main() { os.WriteFile("result", []byte(encoded[0]), 0600) }
