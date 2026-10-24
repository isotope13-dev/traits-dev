package main
import "os"
func write(f *os.File, size int64) {
 buf := make([]byte, 262144)
 for written := int64(0); written < size; written += 262144 {
  f.Write(buf)
 }
}
