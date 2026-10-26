package main
import "os"
func main() { _ = os.Chmod("input", 0600); f, _ := os.Open("input"); if f != nil { _ = f.Chmod(0600) } }
