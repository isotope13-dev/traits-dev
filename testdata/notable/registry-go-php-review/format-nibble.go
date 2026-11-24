package formatting
import "strconv"
func format(n byte) string { return strconv.Itoa(64+int(n&15)) }
