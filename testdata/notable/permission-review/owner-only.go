package settings
import "os"
func Protect() error { return os.Chmod("settings.conf", 0600) }
