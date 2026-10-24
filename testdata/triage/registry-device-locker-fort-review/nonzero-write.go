package main
import "os"
func write(f *os.File, size int64) {
 buf := []byte("content")
 for written := int64(0); written < size; written += 7 {
  f.Write(buf)
 }
}
