package main
import (
    "compress/gzip"
    "io"
    "os"
)
func main() {
    gr, _ := gzip.NewReader(os.Stdin)
    io.Copy(os.Stdout, gr)
}
