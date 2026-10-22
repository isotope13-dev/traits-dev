package main
import "github.com/gopacket/gopacket/pcap"
func main() { handle, _ := pcap.OpenLive("wlan0", 65536, false, pcap.BlockForever); handle.Close() }
