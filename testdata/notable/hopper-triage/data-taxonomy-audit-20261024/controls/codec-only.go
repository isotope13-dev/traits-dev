package main
import (
    "encoding/base64"
    "hash/crc32"
)
func main() {
    _ = base64.NewEncoding("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
    _ = crc32.ChecksumIEEE([]byte("an unrelated checksum"))
}
