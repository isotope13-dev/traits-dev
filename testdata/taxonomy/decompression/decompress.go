package fixture
import (
  "compress/gzip"
  "io"
)
func transform(r io.Reader) { gzip.NewReader(r) }
