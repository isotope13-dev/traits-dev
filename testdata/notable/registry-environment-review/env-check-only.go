package utility
import "os"
func Enabled() bool { return os.Getenv("DEBUG") != "" }
