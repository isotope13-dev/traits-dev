package main
import (
    "bytes"
    "compress/gzip"
    "encoding/base64"
    "io"
    "os"
)
func main() {
    raw, _ := base64.StdEncoding.DecodeString("example")
    gr, _ := gzip.NewReader(bytes.NewReader(raw))
    io.Copy(os.Stdout, gr)
}
