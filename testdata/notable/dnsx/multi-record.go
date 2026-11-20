package sample
import "github.com/projectdiscovery/dnsx/libs/dnsx"
func lookup() { client, _ := dnsx.New(dnsx.Options{}); client.QueryMultiple("changed.example") }
