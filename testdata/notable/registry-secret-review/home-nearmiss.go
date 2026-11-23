package example
import "os"
func clear() {
 home := os.Getenv("HOME_CACHE")
 os.RemoveAll(home)
}
