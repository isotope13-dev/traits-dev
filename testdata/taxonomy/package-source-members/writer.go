package writer
import "io"
type Tokens []byte
func (ts Tokens) WriteTo(w io.Writer) (int64, error) { n, err := w.Write(ts); return int64(n), err }
func render(ts Tokens, w io.Writer) { ts.WriteTo(w) }
