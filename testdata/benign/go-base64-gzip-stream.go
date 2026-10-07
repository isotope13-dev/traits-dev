package assets
import (
  "encoding/base64"
  "compress/gzip"
  "io"
)
func open(r io.Reader) (*gzip.Reader, error) {
  b64 := base64.NewDecoder(base64.StdEncoding, r)
  return gzip.NewReader(b64)
}
