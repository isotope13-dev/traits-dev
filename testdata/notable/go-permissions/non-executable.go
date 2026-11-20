package sample
import "os"
func apply(path string) { os.Chmod(path, 0644) }
