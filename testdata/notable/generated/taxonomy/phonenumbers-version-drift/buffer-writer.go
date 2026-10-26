package formatting
import "bytes"
func render(data []byte) []byte {
 var b bytes.Buffer
 b.Write(data)
 return b.Bytes()
}
