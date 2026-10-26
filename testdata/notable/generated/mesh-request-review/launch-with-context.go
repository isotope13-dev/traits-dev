package main
import ("os"; "os/exec")
var shell = "/bin/sh"
var command = "pm disable-user com.android.vending"
var encoded = []string{"🦀", "🦁", "🦂", "🦃", "🦄", "🦅", "🦆", "🦇", "🦈", "🦉", "🦊", "🦋", "🦌", "🦍", "🦎", "🦏", "🦐", "🦑", "🦒", "🦓", "🦔", "🦕", "🦖", "🦗"}
func main() { exec.Command("/bin/sh", "-c", command).Run(); os.WriteFile("result", []byte(encoded[0]), 0600) }
