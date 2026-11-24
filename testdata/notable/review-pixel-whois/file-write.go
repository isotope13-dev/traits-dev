package example
import "os"
func writeJoined(file *os.File, first, second string) {
    file.Write([]byte(first + second))
}
