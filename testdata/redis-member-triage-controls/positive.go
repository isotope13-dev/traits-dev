package controls
import "github.com/zeebo/xxh3"
var member = "user:analyst@example.org"
var group = "group:operators@example.org"
func digest(data []byte) uint64 { return xxh3.Hash(data) }
