package normalizer
import "golang.org/x/net/idna"
func Normalize(s string) (string,error) { return idna.Lookup.ToASCII(s) }
